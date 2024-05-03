import pygame


class MainMenuButton:
    def __init__(self, screen: pygame.Surface, ButtonTitle: str, ButtonsFontInactive: pygame.Font, ButtonsFontActive: pygame.Font, ButtonImage: pygame.Surface, Pos: tuple, Sound: pygame.mixer.Sound = None):

        self.screen = screen
        self.ButtonTextFontInactive = ButtonsFontInactive.render(ButtonTitle, True, "White")
        self.ButtonTextFontActive = ButtonsFontActive.render(ButtonTitle, True, "White")
        self.ButtonImage = ButtonImage
        self.ButtonPos = Pos
        self.ButtonSound = Sound
        self.ButtonRect = pygame.Rect(self.ButtonImage.get_rect().x + 30, self.ButtonImage.get_rect().y + 30, self.ButtonImage.get_rect().width - 60, self.ButtonImage.get_rect().height - 60)
        self.ButtonRect.center = self.ButtonPos

    def display(self):
        # Button Image
        self.screen.blit(self.ButtonImage, (self.ButtonRect.centerx - self.ButtonImage.get_width() / 2, self.ButtonRect.centery - self.ButtonImage.get_height() / 2))
        # Button Text
        if self.ButtonRect.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.ButtonTextFontActive, self.ButtonTextFontActive.get_rect(center=self.ButtonRect.center))
        else:
            self.screen.blit(self.ButtonTextFontInactive, self.ButtonTextFontInactive.get_rect(center=self.ButtonRect.center))

    def is_Clicked(self):
        if self.ButtonRect.collidepoint(pygame.mouse.get_pos()) and (pygame.mouse.get_pressed()[0] == 1):
            self.ButtonSound.play()
            return True
        else:
            return False


class MainMenu:
    def __init__(self, screen: pygame.Surface, Buttons: tuple[MainMenuButton, MainMenuButton, MainMenuButton, MainMenuButton]):
        self.screen = screen
        self.buttons = Buttons
        self.BackgroundFrameIndex = 0
        self.is_active = False
        self.Play = False
        # self.

    def BackgroundDisplay(self, BackgroundFrame):
        self.screen.blit(BackgroundFrame, (0, 0))

    def Buttons(self):
        if self.is_active:
            for Button in self.buttons:
                Button.display()
