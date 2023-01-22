import pygame.image
from pygame.sprite import Sprite, AbstractGroup
from slicer import get_images
import pyganim

IDLE = "IDLE"
RUN = "RUN"
HIT = "HIT"
D_JUMP = "D_JUMP"
FALL = "FALL"
JUMP = "JUMP"
W_JUMP = "W_JUMP"
all_states = RUN, IDLE, HIT, D_JUMP, FALL, JUMP, W_JUMP
LEFT = "LEFT"
RIGHT = "RIGHT"


class Player(Sprite):
    def __init__(self, pos, game, *groups: AbstractGroup):
        super().__init__(*groups)
        self.game = game
        self.gravity = 3
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 10
        self.jump_force = 40
        self.on_platform = False
        self.state = IDLE
        self.facing = RIGHT
        self.is_running_right = False
        self.is_running_left = False
        self.setup_animation()
        self.image = self.anim_objs[self.state + self.facing].getCurrentFrame()
        self.rect = self.image.get_rect(topleft=pos)
        self.spawn_pos = list(pos)
        self.jumps_total = 2
        self.jumps_left = 0

    def take_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.jumps_left:
                self.direction.y = -self.jump_force
                self.jumps_left -= 1

            if event.key == pygame.K_ESCAPE:
                self.game.switch_to_menu()

            if event.key == pygame.K_d:
                self.is_running_right = True

            if event.key == pygame.K_a:
                self.is_running_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.is_running_right = False

            if event.key == pygame.K_a:
                self.is_running_left = False

        if self.is_running_right and not self.is_running_left:
            self.direction.x = self.speed
            self.facing = RIGHT

        elif self.is_running_left and not self.is_running_right:
            self.direction.x = -self.speed
            self.facing = LEFT

        else:
            self.direction.x = 0

    def setup_animation(self):
        self.anim_objs = {}
        for state in all_states:
            images = get_images(pygame.image.load(f"images/Main Characters/Virtual Guy/{state}.png"), 32, 32, 2)
            imagesAndDurations = [(image, 70) for image in images]
            right_anim = pyganim.PygAnimation(imagesAndDurations)
            left_anim = right_anim.getCopy()
            left_anim.flip(True, False)
            self.anim_objs[state + RIGHT] = right_anim
            self.anim_objs[state + LEFT] = left_anim
        self.state_conductor = pyganim.PygConductor(self.anim_objs)
        self.state_conductor.play()

    def set_state(self):
        if not self.on_platform:
            if self.direction.y < 0:
                if self.jumps_left < self.jumps_total - 1:
                    self.state = D_JUMP
                else:
                    self.state = JUMP
            elif self.direction.y > 0:
                self.state = FALL

        elif self.direction.x != 0:
            self.state = RUN
        else:
            self.state = IDLE

    def update(self, *args, **kwargs):
        self.apply_gravity()
        self.set_state()
        self.image = self.anim_objs[self.state + self.facing].getCurrentFrame()

    def apply_gravity(self):
        self.direction.y += self.gravity

    def respawn(self):
        self.rect.topleft = self.spawn_pos

    def set_spawn_point(self, pos):
        if pos[0] > self.spawn_pos[0]:
            self.spawn_pos = list(pos)
