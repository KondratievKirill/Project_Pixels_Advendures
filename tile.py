import pygame
from slicer import get_images

terrain_image = pygame.image.load("images/Terrain/Terrain (16x16).png").subsurface((96, 0, 80, 48))
lst_of_images = get_images(terrain_image, 16, 16, 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, place_code, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((size, size))
        self.image.fill("grey")
        self.rect = self.image.get_rect(topleft=pos)
        if place_code[1] == 0 and place_code[3] == 0:
            self.image.blit(lst_of_images[0], (0, 0))
        elif place_code[1] == 0 and place_code[3] == 1:
            self.image.blit(lst_of_images[1], (0, 0))
        elif place_code[1] == 1 and place_code[3] == 0:
            self.image.blit(lst_of_images[5], (0, 0))
        elif place_code[1] == 1 and place_code[3] == 1 and place_code[0] == 1:
            self.image.blit(lst_of_images[6], (0, 0))
        elif place_code[1] == 1 and place_code[3] == 1 and place_code[0] == 0:
            self.image.blit(lst_of_images[9], (0, 0))

        if place_code[1] == 0 and place_code[4] == 0:
            self.image.blit(lst_of_images[2], (32, 0))
        elif place_code[1] == 0 and place_code[4] == 1:
            self.image.blit(lst_of_images[1], (32, 0))
        elif place_code[1] == 1 and place_code[4] == 0:
            self.image.blit(lst_of_images[7], (32, 0))
        elif place_code[1] == 1 and place_code[4] == 1 and place_code[2] == 1:
            self.image.blit(lst_of_images[6], (32, 0))
        elif place_code[1] == 1 and place_code[4] == 1 and place_code[2] == 0:
            self.image.blit(lst_of_images[8], (32, 0))

        if place_code[3] == 0 and place_code[6] == 0:
            self.image.blit(lst_of_images[10], (0, 32))
        elif place_code[3] == 0 and place_code[6] == 1:
            self.image.blit(lst_of_images[5], (0, 32))
        elif place_code[3] == 1 and place_code[6] == 0:
            self.image.blit(lst_of_images[11], (0, 32))
        elif place_code[3] == 1 and place_code[6] == 1 and place_code[5] == 1:
            self.image.blit(lst_of_images[6], (0, 32))
        elif place_code[3] == 1 and place_code[6] == 1 and place_code[5] == 0:
            self.image.blit(lst_of_images[4], (0, 32))

        if place_code[4] == 0 and place_code[6] == 0:
            self.image.blit(lst_of_images[12], (32, 32))
        elif place_code[4] == 0 and place_code[6] == 1:
            self.image.blit(lst_of_images[7], (32, 32))
        elif place_code[4] == 1 and place_code[6] == 0:
            self.image.blit(lst_of_images[11], (32, 32))
        elif place_code[4] == 1 and place_code[6] == 1 and place_code[7] == 1:
            self.image.blit(lst_of_images[6], (32, 32))
        elif place_code[4] == 1 and place_code[6] == 1 and place_code[7] == 0:
            self.image.blit(lst_of_images[3], (32, 32))
