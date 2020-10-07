import pygame
from pygame.locals import *
import os
import widget

def load_images(dir, colorkey=None):
    arr = []
    try:
        images = os.listdir(dir)
    except(pygame.error, message):
        print('Cannot load images dir:' + dir)
    for i in images:
        image = pygame.image.load(dir+i)
        image = pygame.transform.scale2x(image)
        arr.append([image, image.get_rect()])
    # image = image.convert()
    # image = image.convert_alpha()
    return arr
    
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.images = load_images("warrior-set/individual-sprite/Run/", -1)
        self.image, self.rect = self.images[self.current_frame]
        self.origin = self.image
        self.screen = pygame.display.get_surface()
        self.step = 10
        self.margin = 12
        self.area = self.screen.get_rect()
        self.xsteps = self.step
        self.ysteps = 0
        self.jumpCount = 20
        self.vel = 10
        self.state = "idle"
        self.m = 2
        self.hitting = 0
        self.degrees = 0
        self.direction = ""
        self.orientation = "right"
        self.coins = 0

    def jump(self):
        # self.state = "jumping"
        # if self.vel > 0:
        #     F = ( 0.25 * self.m * (self.vel*self.vel) )
        # else:
        #     F = -( 0.25 * self.m * (self.vel*self.vel) )
        F = ( 0.25 * self.m * (self.vel*self.vel) )
        self.ysteps = - F
        self.vel = self.vel - 1

    def gravity(self, ground=pygame.sprite.Group()):
        collided = pygame.sprite.spritecollide(self, ground, False)
        if not collided:
            self.ysteps += self.step
        else:
            if self.rect.bottom > collided[0].rect.bottom and self.rect.top >= collided[0].rect.top:
                self.rect.top = collided[0].rect.bottom
            elif self.rect.bottom > collided[0].rect.top:
                self.rect.bottom = collided[0].rect.top
            else:
                self.ysteps = 0
            self.vel = 10

    def key_move(self):
        if self.state == "dead":
            return
        key_pressed = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        self.state = "running"
        if key_pressed[pygame.K_x] or mouse[0]:
            self.hit()
        # if key_pressed[pygame.K_z] or mouse[1]:
        #     self.throw()
        elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            self.ysteps = self.step * 2
            self.direction = "down"
        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.ysteps = -self.step
            self.direction = "up"
        elif key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.xsteps = -self.step
            self.direction = "left"
        elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.xsteps = self.step
            self.direction = "right"
        else:
            self.state = "idle"

    def hit(self):
        self.hitting = 1
        self.xsteps = 0

    def throw(self, widget=widget.Widget()):
        widget.rect.x = self.rect.left + 15
        widget.rect.y = self.rect.y + 15
        widget.active = True

    def __spin(self):
        center = self.rect.center
        self.degrees = self.degrees + 12
        if self.degrees >= 360:
            self.degrees = 0
            self.image = self.original
        else:
            self.image = pygame.transform.rotate(self.original, self.degrees)
        self.rect = self.image.get_rect(center=center)

    def update(self):
        newpos = self.rect.move((self.xsteps, self.ysteps))
        
        if self.state == "idle":
            self.xsteps = 0
            self.ysteps = 0
            self.direction = ""

        self.current_frame += 1
        
        if self.state == "idle":
            self.images = load_images("warrior-set/individual-sprite/Idle/", -1)
        elif self.state == "jumping":
            self.images = load_images("warrior-set/individual-sprite/Jump/", -1)
        if self.direction == "down":
            self.images = load_images("warrior-set/individual-sprite/Fall/", -1)
        elif self.direction == "up":
            self.images = load_images("warrior-set/individual-sprite/Jump/", -1)
        elif self.direction == "right":
            self.orientation = "right"
            self.images = load_images("warrior-set/individual-sprite/Run/", -1)
        elif self.direction == "left":
            self.orientation = "left"
            self.images = load_images("warrior-set/individual-sprite/Run/", -1)
        if self.state == "dead":
            self.images = load_images("warrior-set/individual-sprite/Death-Effect/", -1)
            self.xsteps = 0
        
        if self.hitting == 1:
            self.images = load_images("warrior-set/individual-sprite/Attack/", -1)

        if self.current_frame >= len(self.images):
            if self.state == "dead":
                self.current_frame = len(self.images)-1
            else:
                self.current_frame = 0
        self.image, self.rect = self.images[self.current_frame]
        
        if self.orientation == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = newpos
        # self.gravity()

