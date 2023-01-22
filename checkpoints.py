import pygame
import settings as s
from slicer import get_images


class CheckPoint(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.images = get_images(pygame.image.load(
            "images/Items/Checkpoints/Checkpoint/Checkpoint (Flag Out) (64x64).png"), s.TILE_SIZE,
                                 s.TILE_SIZE)
        self.image = self.images[-1]
        self.rect = self.image.get_rect(topleft=pos)


class FinishLevel(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.images = get_images(pygame.image.load("images/Items/Checkpoints/End/End (Idle).png"), s.TILE_SIZE,
                                 s.TILE_SIZE)
        self.image = self.images[-1]
        self.rect = self.image.get_rect(topleft=pos)


class StartLevel(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.images = get_images(pygame.image.load("images/Items/Checkpoints/Start/Start (Idle).png"), s.TILE_SIZE,
                                 s.TILE_SIZE)
        self.image = self.images[-1]
        self.rect = self.image.get_rect(topleft=pos)
