import pygame

import settings
from background import Background


class NameInput:
    def __init__(self, screen):
        self.fpsClock = pygame.time.Clock()
        self.name = ""
        self.screen = screen
        self.rect = pygame.Rect(100, 100, 500, 200)
        self.font = pygame.font.SysFont("Arial", 20, True)
        self.background = Background("blue")

    def name_input(self):
        while True:
            for event in pygame.event.get(pygame.KEYDOWN):
                letter: str = event.unicode.upper()
                if event.key == pygame.K_RETURN:
                    return self.name
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif letter.isalnum():
                    self.name += letter
            self.text_surface = self.font.render(self.name, True, "red")
            self.text_rect = self.text_surface.get_rect()
            self.text_rect.center = self.rect.center
            self.draw(self.screen)
            pygame.display.flip()
            self.fpsClock.tick(settings.FPS)



    def draw(self, screen):
        self.background.update()
        self.background.rect.x += 1
        self.background.draw(screen)
        pygame.draw.rect(screen, "grey", self.rect)
        screen.blit(self.text_surface, self.text_rect)
