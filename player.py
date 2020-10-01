import pygame
from pygame.locals import *


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except(pygame.error, message):
        print('Cannot load image:' + name)
    # image = image.convert()
    # image = image.convert_alpha()
    return image, image.get_rect()
    
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("warrior-set/individual-sprite/Run/Warrior_Run_1.png", -1)
        self.origin = self.image
        self.screen = pygame.display.get_surface()
        self.step = 1
        self.margin = 12
        self.area = self.screen.get_rect()
        self.xsteps = self.step
        self.ysteps = 0
        self.vel = 8
        self.jumping = False
        self.m = 4
        self.degrees = 0
        self.direction = "right"
        self.orientation = "right"
        self.coins = 0
        self.nhits = 0
        self.nmisses = 0
        # self.image = pygame.transform.rotate(self.original, self.degrees)

    def rect_move(self):
        if self.direction == "right":
            self.orientation = "right"
            self.image = self.origin
        elif self.direction == "down":
            if self.orientation == "right":
                self.image = pygame.transform.rotate(self.origin, -90)
            elif self.orientation == "left":
                self.image = pygame.transform.flip(self.origin, True, False)
                self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "left":
            self.orientation = "left"
            self.image = pygame.transform.flip(self.origin, True, False)
        elif self.direction == "up":
            if self.orientation == "right":
                self.image = pygame.transform.rotate(self.origin, 90)
            elif self.orientation == "left":
                self.image = pygame.transform.flip(self.origin, True, False)
                self.image = pygame.transform.rotate(self.image, -90)

    def __move(self):
        # print(self.direction)
        newpos = self.rect.move((self.xsteps, self.ysteps))

        if self.direction == "right":
            self.image = pygame.transform.rotate(self.origin, -90)
            if self.rect.right > self.area.right - self.margin:
                # self.image = pygame.transform.rotate(self.image, -90)
                self.xsteps = 0
                self.ysteps = self.step
                self.direction = "down"

        elif self.direction == "down":
            self.image = pygame.transform.rotate(self.origin, 180)
            if self.rect.bottom > self.area.bottom - self.margin:
                # self.image = pygame.transform.rotate(self.image, -90)
                self.xsteps = -self.step
                self.ysteps = 0
                self.direction = "left"

        elif self.direction == "left":
            self.image = pygame.transform.rotate(self.image, 90)
            if self.rect.left < self.area.left + self.margin:
                # self.image = pygame.transform.rotate(self.image, -90)
                self.xsteps = 0
                self.ysteps = -self.step
                self.direction = "up"

        elif self.direction == "up":
            self.image = self.origin
            if self.rect.top < self.area.top + self.margin:
                # self.image = pygame.transform.rotate(self.image, -90)
                self.xsteps = self.step
                self.ysteps = 0
                self.direction = "right"
        self.rect_move()
        self.rect = newpos

    def __spin(self):
        center = self.rect.center
        self.degrees = self.degrees + 12
        if self.degrees >= 360:
            self.degrees = 0
            self.image = self.original
        else:
            self.image = pygame.transform.rotate(self.original, self.degrees)
        self.rect = self.image.get_rect(center=center)

    def key_move(self):
        key_pressed = pygame.key.get_pressed()
        newpos = self.rect.move((self.xsteps, self.ysteps))

        if key_pressed[pygame.K_DOWN]:
            # self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = 0
            self.ysteps = self.step
            self.direction = "down"

        elif key_pressed[pygame.K_LEFT]:
            # self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = -self.step
            self.ysteps = 0
            self.direction = "left"

        elif key_pressed[pygame.K_RIGHT]:
            # self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = self.step
            self.ysteps = 0
            self.direction = "right"

        if key_pressed[pygame.K_UP]:
            # self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = 0
            self.ysteps = -self.step
            self.direction = "up"

        self.update()
        self.rect = newpos

    def hit(self):
        # coin.update(self.screen)
        mousex, mousey = pygame.mouse.get_pos()
        collide = False
        bigger_rect = self.rect.inflate(40,40)
        if bigger_rect.collidepoint(mousex, mousey):
            collide = True
        if not self.degrees and collide:
            self.degrees = 1
            self.original = self.image
            self.nhits += 1
            print("hits: %d" %self.nhits)
        else:
            self.nmisses += 1
            print("misses: %d" %self.nmisses)

    def update(self):
        if self.degrees:
            self.__spin()
        else:
            self.__move()
