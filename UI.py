import pygame
import settings as s
import func
import pickle
from name_input import NameInput


class Button:
    def __init__(self, pos, menu):
        self.pos = pos
        self.menu = menu
        self.rect = self.image.get_rect(center=self.pos)
        self.image_2x = pygame.transform.scale2x(self.image)
        self.image_1x = self.image

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_2x
            else:
                self.image = self.image_1x
            self.rect = self.image.get_rect(center=self.rect.center)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.func()

    def func(self):
        pass


class PlayButton(Button):
    def __init__(self, pos, menu):
        self.image = pygame.transform.scale(pygame.image.load(f"images/Menu/Buttons/Play.png"), (150, 150))
        super().__init__(pos, menu)

    def func(self):
        self.menu.game.switch_to_level(self.menu.level_number)


class LevelSelectButton(Button):
    def __init__(self, pos, number, menu):
        self.image = pygame.transform.scale2x(pygame.image.load(f"images/Menu/Levels/{str(number).zfill(2)}.png"))
        self.number = number
        super().__init__(pos, menu)

    def func(self):
        self.menu.select_level(self.number)


class MuteButton(Button):
    def __init__(self, pos, menu):
        self.image = pygame.image.load("images/Menu/Buttons/Volume.png")
        self.is_mute = False
        super().__init__(pos, menu)

    def func(self):
        self.is_mute = not self.is_mute
        if self.is_mute:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(0.45)

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.name_input = NameInput(screen)
        self.load_scores()
        self.select_level(1)
        self.setup_buttons()

    def setup_buttons(self):
        self.buttons = [PlayButton((1000, 300), self)]
        for x in range(5):
            for y in range(5):
                number = y * 5 + x + 1
                self.buttons.append(LevelSelectButton((x * 50 + 600, y * 50 + 150), number, self))

    def load_scores(self):
        try:
            with open('score_boards.pickle', 'rb') as f:
                self.scores = pickle.load(f)
        except FileNotFoundError:
            self.scores = dict()

    def save_scores(self):
        with open('score_boards.pickle', 'wb') as f:
            pickle.dump(self.scores, f)

    def add_best_score(self, time):
        score_board = self.scores.get(self.level_number)
        if not score_board:
            self.scores[self.level_number] = ScoreBoard((time, self.name_input.name_input()))
        elif time < score_board.get_worst_score() or len(score_board) < 5:
            score_board.add((time, self.name_input.name_input()))
        self.save_scores()

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)
        self.minimap.draw()
        if self.level_number in self.scores:
            self.scores[self.level_number].draw(self.screen)

    def run(self):
        self.draw()

    def select_level(self, number):
        self.level_number = number
        self.minimap = MiniMap(self.screen, self.level_number)

    def update_buttons(self, event):
        for button in self.buttons:
            button.update(event)


class MiniMap:
    def __init__(self, screen, num_of_level=1):
        self.num_of_level = num_of_level
        self.screen = screen
        self.create()
        self.phase = 0
        self.step = 15

    def create(self):
        level_layout = s.LEVEL_MAP[self.num_of_level]
        surface = pygame.Surface(
            (
                s.TILE_SIZE * len(level_layout[0]),
                s.TILE_SIZE * len(level_layout)
            )
        )
        div = surface.get_height() / 500
        for row_index, row in enumerate(level_layout):
            for col_index, cell in enumerate(row):
                x = col_index * s.TILE_SIZE
                y = row_index * s.TILE_SIZE
                if cell == "x":
                    pygame.draw.rect(surface, "grey", (x, y, s.TILE_SIZE, s.TILE_SIZE))
                if cell == "F":
                    pygame.draw.circle(surface, "red",
                                       (x + s.TILE_SIZE / 2, y + s.TILE_SIZE / 2),
                                       s.TILE_SIZE / 4)
        self.surface = pygame.transform.scale(surface, (surface.get_width() / div, surface.get_height() / div))

        self.rect = pygame.rect.Rect(20, 20, 500, 500)
        self.bg_rect = self.rect.copy()
        self.bg_rect.width += 30
        self.bg_rect.height += 30
        self.bg_rect.x -= 15
        self.bg_rect.y -= 15

    def draw(self):

        pygame.draw.rect(self.screen, "yellow", self.bg_rect, border_radius=20)
        self.screen.blit(self.surface.subsurface(self.phase, 0, 500, 500), self.rect)
        if self.phase + self.step + self.rect.width <= self.surface.get_width():
            self.phase += self.step
        else:
            self.phase = 0


class ScoreBoard:
    def __init__(self, *scores):
        self.best_times = list(scores)
        self.sort()
        self.name = None

    def __repr__(self):
        return str(self.best_times)

    def add(self, score_name):
        self.best_times.append(score_name)
        self.sort()

    def get_worst_score(self):
        return self.best_times[-1][0]

    def __len__(self):
        return len(self.best_times)

    def sort(self):
        self.best_times.sort()
        self.best_times = self.best_times[:5]

    def draw(self, screen):
        for i, time_name in enumerate(self.best_times):
            func.draw_letters(screen, time_name[1], 2 if i == 0 else 1, topleft=(25, i * 50 + 550))
            func.draw_digits(screen, time_name[0] / 1000, 2 if i == 0 else 1, topleft=(500, i * 50 + 550))


class StartScene:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.image = pygame.Surface((s.WIDTH, s.HEIGHT))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topright=(0, 0))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.rect.right <= s.WIDTH:
            self.rect.x += min(6, s.WIDTH - self.rect.right)

    def take_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.rect.right == s.WIDTH:
                self.game.switch_to_menu()
            else:
                self.rect.right = s.WIDTH

    def run(self):
        self.update()
        self.draw()


class FinalScene:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.image = pygame.Surface((s.WIDTH, s.HEIGHT))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(topright=(0, 0))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.rect.right <= s.WIDTH:
            self.rect.x += min(20, s.WIDTH - self.rect.right)

    def take_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.rect.right == s.WIDTH:
                self.game.switch_to_menu()
            else:
                self.rect.right = s.WIDTH

    def run(self):
        self.update()
        self.draw()


class LivesCounter:
    def __init__(self):
        self.lives = 3
        self.image = pygame.image.load("images/live.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect(midtop=(s.WIDTH / 2, 40))

    def loose_live(self):
        self.lives -= 1

    def get_lives(self):
        return self.lives

    def draw(self, screen):
        for live in range(self.lives):
            self.rect.left = s.WIDTH / 2 - (self.lives / 2 * 80) + live * 90
            screen.blit(self.image, self.rect)
