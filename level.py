import pygame
from pygame.locals import *
import os

def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except(pygame.error, message):
        print('Cannot load image:' + name)
    # image = image.convert()
    return image, image.get_rect()    

class Level(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("warrior-set/tile.png")
        # self.image = pygame.transform.scale(self.image, (25, 25))
        self.xpos = 0
        self.ypos = 0