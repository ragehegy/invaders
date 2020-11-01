import pygame
from pygame.locals import *
import numpy as np

class Game:
    def __init__(self):
        self.height = 600
        self.width = 1000
        self.clock = pygame.time.Clock()
        self.bgcolor = np.random.randint(0, 255, size=(4, 3))[0]
        self.bgimg = pygame.image.load("warrior-set/bg.png")
        self.sound = "sound.wav"
        self.caption = "Animation Demo"

    def init(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        screen.fill(self.bgcolor)
        screen.blit(self.bgimg, (0,0))
        # self.play_audio(self.sound)
        return screen

    def play_audio(self, sound):
        audio = pygame.mixer.Sound(sound)
        audio.play(-1)
        timeout = 1
        pygame.time.delay(timeout * 1000)
    
    def load_image(name, colorkey=None):
        try:
            image = pygame.image.load(name)
        except(pygame.error, message):
            print('Cannot load image:' + name)
        image = image.convert()
        return image, image.get_rect()

    def game_text(self):
        if pygame.font:
            font = pygame.font.Font(None, 18)
            text = font.render("Hit the avatar!", 1, (0, 0, 200))
            textpos = text.get_rect(centerx = int(self.width/2), centery = int(self.height/2))
            return text, textpos

    def pause(self):
        wait = 1
        while wait:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP or e.key == pygame.K_p or e.key == pygame.K_SPACE:
                        wait = 0
                if e.type == pygame.QUIT:
                    return
