import pygame
import settings as s


class Background:
    def __init__(self, color: str):
        self.image = pygame.Surface((s.WIDTH + s.TILE_SIZE, s.HEIGHT))
        self.rect = self.image.get_rect()
        image = pygame.image.load(f"images/Background/{color.capitalize()}.png")
        rect = image.get_rect()
        for j in range(s.HEIGHT // 64):
            for i in range(s.WIDTH // 64 + 1):
                rect.topleft = (i * 64), (j * 64)
                self.image.blit(image, rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x %= -64
