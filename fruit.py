import pygame
import pyganim
import slicer
IDLE = "IDLE"
COLLECTED = "COLLECTED"
ANIM_TYPES = [IDLE, COLLECTED]


class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.fruits_collected = 0
        self.anim_objs = {}
        self.state = IDLE
        self.setup_animation()
        self.image = self.anim_objs[self.state].getCurrentFrame()
        self.rect = self.image.get_rect(topleft=pos)

    def setup_animation(self):
        self.anim_objs = {}
        images = slicer.get_images(pygame.image.load("images/Items/Fruits/Apple.png"), 32, 32, 2)
        imagesAndDurations = [(image, 70) for image in images]
        self.anim_objs[IDLE] = pyganim.PygAnimation(imagesAndDurations)
        self.anim_objs[IDLE].play()

        images = slicer.get_images(pygame.image.load("images/Items/Fruits/Collected.png"), 32, 32, 2)
        imagesAndDurations = [(image, 70) for image in images]
        self.anim_objs[COLLECTED] = pyganim.PygAnimation(imagesAndDurations)
        self.anim_objs[COLLECTED].loop = False

    def is_collected(self):
        return self.state == COLLECTED

    def collect(self):
        self.state = COLLECTED
        self.anim_objs[COLLECTED].play()

    def update(self):
        if self.anim_objs[self.state].isFinished():
            self.kill()
        self.image = self.anim_objs[self.state].getCurrentFrame()
