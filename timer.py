import pygame
import func

digits = [pygame.transform.scale(pygame.image.load(f"images/digits/nums ({num}).png"), (80, 80)) for num in range(10)]
tochka = pygame.transform.scale(pygame.image.load(f"images/digits/dot.png"), (80, 80))


class Timer:
    def __init__(self):
        self.start_time = 0
        self.finish_time = 0
        self.total_time = 0
        self.is_started = False
        self.font = pygame.font.SysFont("Arial", 79)

    def update(self):
        if self.is_started:
            self.total_time = pygame.time.get_ticks() - self.start_time

    def start(self):
        if not self.is_started:
            self.start_time = pygame.time.get_ticks()
            self.is_started = True

    def stop(self):
        if self.is_started:
            self.finish_time = pygame.time.get_ticks()
            self.is_started = False
            return True

    def draw(self, screen):
        func.draw_digits(screen, self.total_time / 1000, 3, topleft=(30, 30))