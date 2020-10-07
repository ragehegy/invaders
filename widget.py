import pygame
from pygame.locals import *
import os

def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except(pygame.error, message):
        print('Cannot load image:' + name)
    image = pygame.transform.scale(image, (50, 50))
    return image, image.get_rect()    

class Widget(pygame.sprite.Sprite):

    def __init__(self, xpos=0, ypos=0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("warrior-set/sword.png")
        self.rect.x = xpos
        self.rect.y = ypos
        self.active = False
        self.stepcount = 0

    def move(self):
        self.active = True
        if self.stepcount == 50:
            self.stepcount = 0
            self.active = False
        else:
            self.rect.x += 15
        self.stepcount += 1
        self.__spin()
    
    def __spin(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.image, -90)