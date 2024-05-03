import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((400, 400))


class Player:
    def __init__(self, Screen: pygame.Surface, image_path):
        self.screen = Screen
        self.image = {
            'up': [(pygame.image.load(f"{image_path}/up/{i}.png").convert_alpha()) for i in range(13, 17)],
            'down': [pygame.image.load(f"{image_path}/down/{i}.png").convert_alpha() for i in range(1, 5)],
            'left': [pygame.image.load(f"{image_path}/left/{i}.png").convert_alpha() for i in range(5, 9)],
            'right': [pygame.image.load(f"{image_path}/right/{i}.png").convert_alpha() for i in range(9, 13)]
        }
        self.direction = 'down'
        self.is_pressed = False

    def animate(self, TimePassed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction = 'up'
            self.is_pressed = True
        elif keys[pygame.K_DOWN]:
            self.direction = 'down'
            self.is_pressed = True
        elif keys[pygame.K_LEFT]:
            self.direction = 'left'
            self.is_pressed = True
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'
            self.is_pressed = True
        else:
            self.is_pressed = False
        rect = [self.image[self.direction][i].get_rect(center=(200, 200)) for i in range(4)]
        if self.is_pressed:
            frame_index = int((int(TimePassed) % 400) / 100)
            self.screen.blit(self.image[self.direction][frame_index], rect[frame_index])
        else:
            self.screen.blit(self.image[self.direction][0], rect[0])


player = Player(screen, "../../media/images/Player")
start_ticks = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("Black")
    player.animate(pygame.time.get_ticks() - start_ticks)

    pygame.display.update()
