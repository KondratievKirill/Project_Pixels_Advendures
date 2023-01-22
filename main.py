import sys

import pygame

import settings as s

from game import Game

pygame.init()

fps = s.FPS
fpsClock = pygame.time.Clock()

width, height = s.WIDTH, s.HEIGHT
screen = pygame.display.set_mode((width, height))
game = Game(screen)
# Game loop.
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        game.take_input(event)
    game.run()
    pygame.display.flip()
    fpsClock.tick(fps)

