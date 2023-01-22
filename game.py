import pygame

import settings as s
from level import Level
from UI import Menu, MuteButton, StartScene, FinalScene


class Game:
    def __init__(self, screen):
        pygame.mixer.music.load("sounds/main_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.40)

        self.start_scene = StartScene(screen, self)
        self.final_scene = FinalScene(screen, self)
        self.level = Level(s.LEVEL_MAP[1], screen, self)
        self.menu = Menu(screen, self)
        self.mute_button = MuteButton((1800, 700), self.menu)
        self.state = START_SCENE
        self.screen = screen

    def switch_to_level(self, level_number):
        self.level = Level(s.LEVEL_MAP[level_number], self.screen, self)
        self.state = GAME

    def switch_to_menu(self):
        self.state = MENU

    def switch_to_final_scene(self):
        self.state = FINAL_SCENE

    def take_input(self, event):
        self.mute_button.update(event)
        if self.state == MENU:
            self.menu.update_buttons(event)
        elif self.state == GAME:
            self.level.take_input(event)
        elif self.state == START_SCENE:
            self.start_scene.take_input(event)
        elif self.state == FINAL_SCENE:
            self.final_scene.take_input(event)

    def final(self):
        self.final_scene.run()

    def run(self):
        if self.state == START_SCENE:
            self.start_scene.run()
        elif self.state == MENU:
            self.menu.run()
        elif self.state == GAME:
            self.level.run()
        elif self.state == FINAL_SCENE:
            self.final_scene.run()
        self.mute_button.draw(self.screen)


MENU = "menu"
GAME = "game"
START_SCENE = "start_scene"
FINAL_SCENE = "final_scene"
