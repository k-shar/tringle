import pygame
from constants import *
from window_sizing import *
import numpy as np
from pygame import freetype

class Dot(pygame.sprite.Sprite):
    def __init__(self, spawn, color):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.color = color
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = spawn[0]*500, spawn[1]*500

        self.held = False

    def update(self):
        self.image.fill(self.color)

        if self.held:
            mouse = pygame.mouse.get_pos()
            self.rect.centerx = mouse[0]
            self.rect.centery = mouse[1]
            self.image.fill(WHITE)


def game(screen):
    clock = pygame.time.Clock()
    pygame.display.set_caption("Game Screen")

    head = Dot((0.5, 0.5), BLACK)

    left = Dot((0.5, 0.8), BLUE)
    right = Dot((0.8, 0.4), BLUE)
    top = Dot((0.2, 0.2), BLUE)

    dots = pygame.sprite.Group()
    dots.add(head)
    dots.add(left)
    dots.add(right)
    dots.add(top)

    sum = TextWindow(BLUE, (25,1), (0.5,0.9), 2, "")
    negative = TextWindow(GREEN, (20,1), (0.5,0.1), 2, "")

    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 500, 'h': 500}))
    while True:
        screen.fill("#A5C2DC")
        dots.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return screen
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                sum.resize(screen)
                negative.resize(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in dots.sprites():
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        sprite.held = True

            if event.type == pygame.MOUSEBUTTONUP:
                for sprite in dots.sprites():
                    sprite.held = False

        A = np.array([[left.rect.x - top.rect.x, right.rect.x - top.rect.x],
                      [left.rect.y - top.rect.y, right.rect.y - top.rect.y]])

        B = np.array([[head.rect.x - top.rect.x],
                      [head.rect.y - top.rect.y]])

        C = np.matmul(np.linalg.inv(A), B)


        # sides
        pygame.draw.line(screen, BLACK, [top.rect.x, top.rect.y], [left.rect.x, left.rect.y], 5)
        pygame.draw.line(screen, BLACK, [top.rect.x, top.rect.y], [right.rect.x, right.rect.y], 5)

        # two scalar lines
        coordT = [top.rect.x, top.rect.y]

        compL = [(left.rect.x-coordT[0]) * C[0], (left.rect.y-coordT[1]) * C[0]]
        compR = [(right.rect.x-coordT[0]) * C[1], (right.rect.y-coordT[1]) * C[1]]

        pygame.draw.line(screen, RED, coordT, [compL[0]+coordT[0], compL[1]+coordT[1]], 10)
        pygame.draw.line(screen, RED,
                         [compL[0]+coordT[0], compL[1]+coordT[1]],
                         (compL[0]+compR[0]+coordT[0], compL[1]+compR[1]+coordT[1]), 10)

        # connecting line
        pygame.draw.line(screen, GREEN, (right.rect.x, right.rect.y), (left.rect.x, left.rect.y), 5)
        dots.draw(screen)

        sum.text = "|sum of scalars| = " + str(C[0]+C[1])[1:6]
        if float(C[0]+C[1]) > 1 or float(C[0]+C[1]) < 0:
            sum.color = RED
        else:
            sum.color = GREEN

        sum.resize(screen)

        count = 0
        for i in C:
            if i<0:
                count += 1

        if count == 0:
            negative.text = f"0 scalars are negative"
            negative.color = GREEN

        if count == 1:
            negative.text = f"1 scalar is negative"
            negative.color = RED

        if count == 2:
            negative.text = f"2 scalars are negative"
            negative.color = RED
        negative.resize(screen)

        screen.blit(sum.image, (sum.rect.x, sum.rect.y))
        screen.blit(negative.image, (negative.rect))
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    pygame.display.init()
    pygame.freetype.init()
    main_screen = pygame.display.set_mode((300, 200), pygame.RESIZABLE)
    game(main_screen)
    pygame.quit()
