import pygame
import settings as s
from player import Player
from tile import Tile
from checkpoints import CheckPoint, StartLevel, FinishLevel
from fruit import Fruit
from timer import Timer
from UI import LivesCounter
import func
from background import Background


class Level:
    def __init__(self, level_map, display_surface, game):
        self.game = game
        self.lives_counter = LivesCounter()
        self.display_surface = display_surface
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.start = pygame.sprite.GroupSingle()
        self.finish = pygame.sprite.GroupSingle()
        self.check_points = pygame.sprite.Group()
        self.keys = pygame.sprite.GroupSingle()
        self.background = Background("green")
        self.score = 0
        self.timer = Timer()
        self.right_trigger = s.WIDTH * 3 / 4
        self.left_trigger = s.WIDTH * 1 / 4
        self.level_map = level_map
        self.setup_level(level_map)
        self.load_sounds()

    def load_sounds(self):
        self.finish_sound = pygame.mixer.Sound("sounds/finish.mp3")
        self.pick_up_sound = pygame.mixer.Sound("sounds/pick_up.mp3")
        self.jump_sound = pygame.mixer.Sound("sounds/jump.mp3")

    def setup_level(self, layout: list):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * s.TILE_SIZE
                y = row_index * s.TILE_SIZE
                if cell == "x":
                    place_code = func.get_placement_code(layout, row_index, col_index)
                    self.tiles.add(Tile((x, y), s.TILE_SIZE, place_code))
                if cell == "s":
                    self.start.add(StartLevel((x, y)))
                    self.player.add(Player((x - s.TILE_SIZE * 2, y), self.game))
                if cell == "f":
                    self.finish.add(FinishLevel((x, y)))
                if cell == "c":
                    self.check_points.add(CheckPoint((x, y)))
                if cell == "F":
                    self.fruits.add(Fruit((x, y)))

    def take_input(self, event):
        player: Player = self.player.sprite
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.switch_to_menu()
        player.take_input(event)

    def vertical_movement_collisions(self):
        player: Player = self.player.sprite
        player.rect.y += player.direction.y
        player.on_platform = False
        for tile in self.tiles.sprites():
            if player.rect.colliderect(tile):
                if player.direction.y > 0:
                    player.jumps_left = player.jumps_total
                    player.rect.bottom = tile.rect.top
                    player.on_platform = True
                if player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                player.direction.y = 0
        if player.rect.centery >= s.HEIGHT:
            self.lives_counter.loose_live()
            if self.lives_counter.get_lives() > 0:
                player.respawn()
            else:
                self.game.switch_to_final_scene()

    def horizontal_movement_collisions(self):
        player: Player = self.player.sprite
        player.rect.x += player.direction.x
        for tile in self.tiles.sprites():
            if player.rect.colliderect(tile):
                if player.direction.x > 0:
                    player.rect.right = tile.rect.left
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right

    def player_start_collision(self):
        player: Player = self.player.sprite
        if player.rect.colliderect(self.start.sprite):
            self.timer.start()

    def player_finish_collision(self):
        player: Player = self.player.sprite
        if player.rect.colliderect(self.finish.sprite):
            if self.timer.stop():
                self.game.menu.add_best_score(self.timer.total_time)
                self.finish_sound.play()

    def player_fruit_collision(self):
        player: Player = self.player.sprite
        fruit: Fruit
        for fruit in self.fruits:
            if player.rect.colliderect(fruit):
                if not fruit.is_collected():
                    self.score += 1
                    fruit.collect()
                    self.pick_up_sound.play()

    def shift_tiles(self, d_x):
        for tile in self.tiles:
            tile.rect.x += d_x

    def shift_points(self, d_x):
        for point in self.check_points:
            point.rect.x += d_x
        self.start.sprite.rect.x += d_x
        self.finish.sprite.rect.x += d_x

    def shift_fruits(self, d_x):
        for fruit in self.fruits:
            fruit.rect.x += d_x

    def shift_level(self):
        player: Player = self.player.sprite
        d_x = 0
        if player.rect.centerx > self.right_trigger:
            d_x = self.right_trigger - player.rect.centerx

        if player.rect.centerx < self.left_trigger:
            d_x = self.left_trigger - player.rect.centerx
        if d_x != 0:
            self.shift_tiles(d_x)
            self.shift_points(d_x)
            self.shift_fruits(d_x)
            player.rect.x += d_x
            player.spawn_pos[0] += d_x
            self.background.rect.x += d_x * 0.3

    def points_check(self):
        player: Player = self.player.sprite
        for point in self.check_points:
            if player.rect.colliderect(point):
                player.set_spawn_point(point.rect.topleft)

    def run(self):
        self.player.update()
        self.fruits.update()
        self.timer.update()
        self.vertical_movement_collisions()
        self.horizontal_movement_collisions()
        self.player_start_collision()
        self.player_finish_collision()
        self.player_fruit_collision()
        self.points_check()
        self.shift_level()
        self.background.update()

        self.background.draw(self.display_surface)
        self.check_points.draw(self.display_surface)
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.fruits.draw(self.display_surface)
        self.finish.draw(self.display_surface)
        self.start.draw(self.display_surface)
        self.timer.draw(self.display_surface)
        self.keys.draw(self.display_surface)
        self.lives_counter.draw(self.display_surface)
        func.draw_digits(self.display_surface, self.score, 3, topright=(s.WIDTH - 30, 30))
