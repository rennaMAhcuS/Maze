import pygame


class Preferences:
    def __init__(self, screen: pygame.Surface, MusicState: bool = True):
        self.screen = screen
        self.MusicState = MusicState
        self.is_active = False
