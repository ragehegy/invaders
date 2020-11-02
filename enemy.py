import pygame
from pygame.locals import *
import os

def load_images(dir, colorkey=None):
    arr = []
    try:
        images = os.listdir(dir)
    except(pygame.error, message):
        print('Cannot load images dir:' + dir)
    for i in images:
        image = pygame.image.load(dir+i)
        image = image.convert_alpha()
        arr.append([image, image.get_rect()])
    return arr
    
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.images = load_images("warrior-set/individual-sprite/enemy/", -1)
        self.image, self.rect = self.images[self.current_frame]
        self.origin = self.image
        self.screen = pygame.display.get_surface()
        self.step = 10
        self.margin = 12
        self.area = self.screen.get_rect()
        self.xsteps = self.step
        self.ysteps = 0
        self.jumpCount = 20
        self.stepcount = 0
        self.vel = 10
        self.state = "idle"
        self.m = 2
        self.hitting = 0
        self.degrees = 0
        self.direction = ""
        self.orientation = "right"
        self.coins = 0

    def jump(self):
        self.state = "jumping"
        if self.vel > 0:
                F = ( 0.25 * self.m * (self.vel*self.vel) )
        else:
            F = -( 0.25 * self.m * (self.vel*self.vel) )
        self.ysteps = - F
        self.vel = self.vel - 1
        # else:
        #     self.state = "running"
        #     self.jumpCount = 20
        # self.jumpCount -= 1

    def gravity(self, ground=pygame.sprite.Group()):
        collided = pygame.sprite.spritecollide(self, ground, False)
        if not collided:
            self.ysteps += self.step
        else:
            if self.rect.bottom > collided[0].rect.y:
                self.rect.bottom = collided[0].rect.y
            else:
                self.ysteps = 0
            # self.jumpCount = 20
            self.vel = 10

    def move(self):
        newpos = self.rect.move((self.xsteps, self.ysteps))
        self.state = "running"
        if self.stepcount > 20:
            if self.stepcount == 40:
                self.stepcount = 0
            else:
                self.xsteps = -self.step
                self.direction = "left"
        else:
            self.xsteps = self.step
            self.direction = "right"
        self.stepcount += 1

    def hit(self):
        self.hitting = 1
        self.xsteps = 0

    def update(self):
        newpos = self.rect.move((self.xsteps, self.ysteps))
        
        if self.state == "idle":
            self.xsteps = 0
            self.ysteps = 0
            self.direction = ""

        self.current_frame += 1
        
        if self.state == "idle":
            self.images = load_images("warrior-set/individual-sprite/enemy/", -1)

        if self.current_frame >= len(self.images):
            self.current_frame = 0
        self.image, self.rect = self.images[self.current_frame]
        
        if self.direction == "right":
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = newpos
        # self.gravity()

