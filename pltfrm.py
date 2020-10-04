import pygame
from pygame.locals import *
import os

def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except(pygame.error, message):
        print('Cannot load image:' + name)
    # image = image.convert()
    image = pygame.transform.scale(image, (50, 50))
    return image, image.get_rect()    

class pltfrm(pygame.sprite.Sprite):

    def __init__(self, xpos=0, ypos=0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("warrior-set/ground-tile.png")
        self.rect.x = xpos
        self.rect.y = ypos