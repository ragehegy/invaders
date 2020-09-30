import pygame
from pygame.locals import *
import numpy as np

def play_audio(wav):
    audio = pygame.mixer.Sound(wav)
    audio.play(-1)
    timeout = 1
    # pygame.time.delay(timeout * 1000)
    # audio.stop()
    # audio.sleep(timeout)

def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except(pygame.error, message):
        print('Cannot load image:' + name)
    image = image.convert()
    return image, image.get_rect()

class Invader(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("invader.gif", -1)
        self.screen = pygame.display.get_surface()
        self.step = 9
        self.margin = 12
        self.area = self.screen.get_rect()
        self.xsteps = self.step
        self.ysteps = 0
        self.degrees = 0
        self.direction = "right"
        self.coins = 0
        self.nhits = 0
        self.nmisses = 0
        # self.image = pygame.transform.rotate(self.original, self.degrees)

    def __move(self):
        # print(self.direction)
        newpos = self.rect.move((self.xsteps, self.ysteps))

        if self.direction == "right" and self.rect.right > self.area.right - self.margin:
            self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = 0
            self.ysteps = self.step
            self.direction = "down"

        if self.direction == "down" and self.rect.bottom > self.area.bottom - self.margin:
            self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = -self.step
            self.ysteps = 0
            self.direction = "left"

        if self.direction == "left" and self.rect.left < self.area.left + self.margin:
            self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = 0
            self.ysteps = -self.step
            self.direction = "up"

        if self.direction == "up" and self.rect.top < self.area.top + self.margin:
            self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = self.step
            self.ysteps = 0
            self.direction = "right"
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
            self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = 0
            self.ysteps = self.step
            self.direction = "down"

        elif key_pressed[pygame.K_LEFT]:
            self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = -self.step
            self.ysteps = 0
            self.direction = "left"

        elif key_pressed[pygame.K_UP]:
            self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = 0
            self.ysteps = -self.step
            self.direction = "up"

        elif key_pressed[pygame.K_RIGHT]:
            self.image = pygame.transform.rotate(self.image, -90)
            self.xsteps = self.step
            self.ysteps = 0
            self.direction = "right"

        self.__move()
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

def main():
    sound = "sound.wav"
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Sprite Demo")
    play_audio(sound)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    if pygame.font:
        font = pygame.font.Font(None, 18)
        text = font.render("Hit the avatar!", 1, (0, 0, 200))
        textpos = text.get_rect(centerx = int(background.get_width()/2), centery = int(background.get_height()/2))
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    head = Invader()
    sprite = pygame.sprite.RenderPlain(head)
    
    while True:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                head.hit()
            elif event.type == KEYDOWN:
                head.key_move()

        sprite.update()
        screen.blit(background, (0, 0))
        # screen.blit(coin.image, coin.rect)
        sprite.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()