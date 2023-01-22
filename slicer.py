import pygame


def get_images(image: pygame.Surface, width, height, scale=1):
    lst_of_images = []
    rect_image = image.get_rect()
    w = rect_image.width // width
    h = rect_image.height // height
    rect = pygame.Rect(0, 0, width, height)
    for j in range(h):
        for i in range(w):
            rect.topleft = i * width, j * height
            cut = image.subsurface(rect)
            cut = pygame.transform.scale(cut, (width * scale, height * scale))
            lst_of_images.append(cut)
    return lst_of_images
