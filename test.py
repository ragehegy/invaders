import pygame
from pygame.locals import *
import numpy as np

height = 600
width = 1000
clock = pygame.time.Clock()
bgcolor = np.random.randint(0, 255, size=(4, 3))[0]

pygame.init()
screen = pygame.display.set_mode((width, height))
screen = pygame.transform.chop(screen, (200,200,200,200))
screen.fill(bgcolor)

while True:
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        quit()
    # pygame.time.Clock().tick(20)
    screen.fill(bgcolor)
    pygame.display.flip()