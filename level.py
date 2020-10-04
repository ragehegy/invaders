import pygame
from pygame.locals import *
import pltfrm

class Level:
    def ground(self, screen_w=0, screen_h=0):
        ground_list = pygame.sprite.Group()
        x=0
        ground_sample = pltfrm.pltfrm()
        tile_width = ground_sample.rect.size[0]
        tile_height = ground_sample.rect.size[1]
        for i in range(int(screen_w/tile_width)):
            ground_sample = pltfrm.pltfrm(xpos=x, ypos=screen_h-tile_height)
            ground_list.add(ground_sample)
            x += 50
        ground_list.add(pltfrm.pltfrm(xpos=300, ypos=300))
        return ground_list