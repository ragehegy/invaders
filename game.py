import pygame
from pygame.locals import *
import numpy as np

class Game:
    def __init__(self):
        self.dimensions = [1000, 600]
        # self.width = 1000
        self.clock = pygame.time.Clock()
        self.bgcolor = np.random.randint(0, 255, size=(4, 3))[0]
        self.bgimg = pygame.image.load("warrior-set/bg.png")
        self.sound = "sound.wav"
        self.caption = "Invaders"
        self.captions = ["Press x to attack", "Press z to throw"]
        self.display_info = ""

    def init(self):
        pygame.init()
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption(self.caption)
        self.display_info = pygame.display.Info()
        self.dimensions = [self.display_info.current_w, self.display_info.current_h]
        self.bgimg = pygame.transform.scale(self.bgimg, self.dimensions)
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
            font = pygame.font.Font(None, 28)
            text = font.render(self.caption, 1, (0, 0, 0))
            textpos = text.get_rect(centerx = int(self.dimensions[0]/8), centery = int(self.dimensions[1]-200))
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
