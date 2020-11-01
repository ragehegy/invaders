import pygame
from pygame.locals import *
import pltfrm

class Level:
    def __init__(self, screen_w=0, screen_h=0, tiles=pygame.sprite.Group()):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.tiles = tiles

    def ground(self):
        x=0
        ground_sample = pltfrm.pltfrm()
        tile_width = ground_sample.rect.size[0]
        tile_height = ground_sample.rect.size[1]
        for i in range(int(self.screen_w/tile_width)):
            ground_sample = pltfrm.pltfrm(xpos=x, ypos=self.screen_h-tile_height)
            self.tiles.add(ground_sample)
            x += 50
        return self.tiles
    
    def build(self):
        self.ground()
        _sample = pltfrm.pltfrm(xpos=300, ypos=300)
        self.tiles.add(pltfrm.pltfrm(xpos=300, ypos=300), pltfrm.pltfrm(xpos=350, ypos=500))
        return self.tiles