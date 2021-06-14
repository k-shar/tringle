import pygame
from constants import *
##

def game(screen):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Game Screen")

    while True:
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return screen
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    pygame.display.init()
    main_screen = pygame.display.set_mode((300, 200), pygame.RESIZABLE)
    game(main_screen)
    pygame.quit()
