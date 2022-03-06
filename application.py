import random

import pygame

WIDTH = 480
HEIGHT = 360
FPS = 10

pg = pygame.init()

running = True
background = [120, 120, 120]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(background)
pygame.display.set_caption('Card Heroes 3.0')
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN:
                background = list(map(lambda x: max(0, x - 20), background))
            if e.key == pygame.K_UP:
                background = list(map(lambda x: min(255, x + 20), background))
        if e.type == pygame.MOUSEBUTTONDOWN:
            background = list(map(lambda x: random.Random().randint(0, 255), background))
    screen.fill(background)
    pygame.display.flip()

pygame.quit()
