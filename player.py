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
        self.vel = 30
        self.state = "idle"
        self.m = 1
        self.degrees = 0
        self.direction = ""
        self.orientation = "right"
        self.coins = 0
        self.nhits = 0
        self.nmisses = 0

    def rect_move(self):
        
        self.current_frame += 1

        if self.state == "idle":
            self.images = load_images("warrior-set/individual-sprite/Idle/", -1)

        elif self.state == "jumping":
            # self.direction = "up"
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

        if self.current_frame >= len(self.images):
            self.current_frame = 0

        self.image, self.rect = self.images[self.current_frame]
        
        if self.orientation == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        self.state = "jumping"
        if self.jumpCount > 0:
            if self.jumpCount > 10:
                self.ysteps = -self.vel
            elif self.jumpCount <= 10:
                self.ysteps = self.vel
            self.vel -= 2
        else:
            self.state = "running"
            self.jumpCount = 20
        self.jumpCount -= 1

    def gravity(self):
        if self.rect.top <= 500:
            self.ysteps += self.step
        else:
            self.rect.top = 500
            self.jumpCount = 20
            self.vel = 30

    def key_move(self):
        print(self.rect.top)
        key_pressed = pygame.key.get_pressed()
        newpos = self.rect.move((self.xsteps, self.ysteps))
        
        # if key_pressed[pygame.K_SPACE]:
            
        if key_pressed[pygame.K_DOWN]:
            self.state = "running"
            self.ysteps = self.step
            self.direction = "down"
        elif key_pressed[pygame.K_UP]:
            self.state = "running"
            self.ysteps = -self.step
            self.direction = "up"
        elif key_pressed[pygame.K_LEFT]:
            self.state = "running"
            self.xsteps = -self.step
            self.direction = "left"
        elif key_pressed[pygame.K_RIGHT]:
            self.state = "running"
            self.xsteps = self.step
            self.direction = "right"
        else:
            self.state = "idle"

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
        # if self.degrees:
        #     self.__spin()
        # else:
        #     self.__move()
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

        if self.current_frame >= len(self.images):
            self.current_frame = 0
        self.image, self.rect = self.images[self.current_frame]
        
        if self.orientation == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = newpos
        self.gravity()

