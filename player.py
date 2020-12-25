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
        # image = pygame.transform.scale2x(image)
        image = pygame.transform.scale(image, (50, 50))
        # image = image.convert_alpha()
        arr.append([image, image.get_rect()])
    return arr
    
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.images = load_images("warrior-set/individual-sprite/Run/", -1)
        self.image, self.rect = self.images[self.current_frame]
        self.origin = self.image
        self.step = 10
        self.xsteps = self.step
        self.ysteps = 0
        self.jumpCount = 6
        self.vel = 10
        self.state = "idle"
        self.m = 2
        self.hitting = 0
        self.degrees = 0
        self.health = 5
        self.direction = {
                "right": 0,
                "left": 0,
                "top": 0,
                "bottom": 0,
            }
        self.collision_sides = {
                "right": 0,
                "left": 0,
                "top": 0,
                "bottom": 0,
            }
        self.orientation = "right"
        self.F = ( 0.175 * self.m * pow(self.vel, 2) )

    def jump(self):
        if self.jumpCount > 0:
            self.jumpCount -= 1
            if self.vel > 9:
                self.ysteps = -self.F
                self.vel -= 1
            else:
                return
    
    def detect_collision(self, tiles):
        self.collision_sides = {
            "right": 0,
            "left": 0,
            "top": 0,
            "bottom": 0,
        }

        self.rect.move_ip((self.xsteps, 0))
        

        col = pygame.sprite.spritecollide(self, tiles, False)
        for collision in tiles:
            if self.rect.colliderect(collision.rect):
                if self.xsteps > 0:
                    self.rect.right = collision.rect.left
                    self.collision_sides["right"] = 1
                    self.xsteps = 0
                elif self.xsteps < 0:
                    self.rect.left = collision.rect.right
                    self.collision_sides["left"] = 1
                    self.xsteps = 0
        self.rect.move_ip((0,self.ysteps))
        col = pygame.sprite.spritecollide(self, tiles, False)
        for collision in tiles:
            if self.rect.colliderect(collision.rect):
                if self.ysteps > 0:
                    self.rect.bottom = collision.rect.top
                    self.collision_sides["bottom"] = 1
                    self.ysteps = 0
                elif self.ysteps < 0:
                    self.rect.top = collision.rect.bottom
                    self.collision_sides["top"] = 1
                self.ysteps = 0
        # print(self.collision_sides)
    
    def gravity(self):
        if self.collision_sides["bottom"] == 1  :
            self.vel = 10
        else:
            if self.ysteps < 60:
                self.ysteps += 9
            else:
                self.ysteps = 60

    def move(self, tiles):
        
        if self.state == "dead":
            return

        self.state = "running"
        if self.direction["bottom"] == 1 :
            self.ysteps = self.step * 2
        if self.direction["top"] == 1 :
            self.ysteps = -3*self.step
        if self.direction["left"] == 1 :
            self.xsteps = -self.step
        if self.direction["right"] == 1 :
            self.xsteps = self.step
        self.detect_collision(tiles)
        self.gravity()

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

    def hurt(self):
        print(self.health)
        if self.health <= 0:
            self.state = "dead"
        else:
            return
        # self.health -= 1

    def update(self, tiles):

        self.current_frame += 1
        if self.direction["right"] == 1:
            self.orientation = "right"
            self.images = load_images("warrior-set/individual-sprite/Run/", -1)
        if self.direction["left"] == 1:
            self.orientation = "left"
            self.images = load_images("warrior-set/individual-sprite/Run/", -1)
        if self.state == "jumping":
            self.images = load_images("warrior-set/individual-sprite/Jump/", -1)
        if self.direction["bottom"] == 1:
            self.images = load_images("warrior-set/individual-sprite/Fall/", -1)
        if self.direction["top"] == 1:
            self.images = load_images("warrior-set/individual-sprite/Jump/", -1)
        if self.state == "hurt":
            self.images = load_images("warrior-set/individual-sprite/Hurt-Effect/", -1)
        if self.state == "dead":
            self.images = load_images("warrior-set/individual-sprite/Death-Effect/", -1)
            # self.images = load_images("warrior-set/individual-sprite/Hurt-Effect/", -1)
            self.xsteps = 0
            if self.current_frame == len(self.images) - 1:
                return
        if self.hitting == 1:
            self.images = load_images("warrior-set/individual-sprite/Attack/", -1)

        if self.current_frame >= len(self.images):
            if self.state == "dead":
                self.current_frame = len(self.images)-1
            else:
                self.current_frame = 0
        self.image = self.images[self.current_frame][0]
        if self.orientation == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        
        if self.state == "idle":
            self.xsteps = 0
            self.direction = {
                "right": 0,
                "left": 0,
                "top": 0,
                "bottom": 0,
            }
            self.images = load_images("warrior-set/individual-sprite/Idle/", -1)
            
        self.move(tiles)