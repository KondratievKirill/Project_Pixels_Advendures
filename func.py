import pygame

import slicer


def draw_digits(screen, number, font_size, **kwargs):
    if font_size == 1:
        digits = small_digits
        tochka = small_tochka
    elif font_size == 2:
        digits = medium_digits
        tochka = medium_tochka
    elif font_size == 3:
        digits = big_digits
        tochka = big_tochka
    else:
        print("font size must be int [1:3]")
        return
    surface = pygame.Surface((digits[0].get_width() * len(str(number)), digits[0].get_height()))
    surface.set_colorkey("black")

    for i, ell in enumerate(str(number)):
        if ell != ".":
            image = digits[int(ell)]
        else:
            image = tochka
        rect = image.get_rect(topleft=(i * digits[0].get_width(), 0))
        surface.blit(image, rect)
    rect = surface.get_rect(**kwargs)
    screen.blit(surface, rect)


def get_placement_code(level_map, row, col):
    lst = []
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if i < 0 or j < 0 or i > len(level_map) - 1 or j > len(level_map[0]) - 1:
                lst.append(0)
                continue
            if i == row and j == col:
                continue
            if level_map[i][j] == "x":
                lst.append(1)
            else:
                lst.append(0)

    return lst


def draw_letters(screen, sentence, font_size, **kwargs):
    if font_size == 2:
        letters = medium_letters
    elif font_size == 1:
        letters = small_letters
    else:
        print("font size must be int[1:2]")
        return
    surface = pygame.Surface((letters[0].get_width() * len(sentence), letters[0].get_height()))
    surface.set_colorkey("black")
    for i, ell in enumerate(sentence):
        image = letters[ord(ell) - 65]
        rect = image.get_rect(topleft=(i * image.get_width(), 0))
        surface.blit(image, rect)
    rect = surface.get_rect(**kwargs)
    screen.blit(surface, rect)


*small_digits, small_tochka = slicer.get_images(pygame.image.load("images/Menu/Text/Text (White) (8x10).png"), 8, 10,
                                                3)[30:41]
*medium_digits, medium_tochka = slicer.get_images(pygame.image.load("images/Menu/Text/Text (White) (8x10).png"), 8, 10,
                                                  5)[30:41]
*big_digits, big_tochka = slicer.get_images(pygame.image.load("images/Menu/Text/Text (White) (8x10).png"), 8, 10, 8)[
                          30:41]
medium_letters = slicer.get_images(pygame.image.load("images/Menu/Text/Text (White) (8x10).png"), 8, 10, 5)[:26]
small_letters = slicer.get_images(pygame.image.load("images/Menu/Text/Text (White) (8x10).png"), 8, 10, 3)[:26]
