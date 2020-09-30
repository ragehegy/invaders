import pygame, sys
from pygame.locals import *
import numpy as np

def play_audio(wav):
    audio = pygame.mixer.Sound(wav)
    audio.play(-1)
    timeout = 1
    pygame.time.delay(timeout * 1000)
    audio.stop()
    audio.sleep(timeout)

colors = np.random.randint(0, 255, size=(4, 3))
white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Animation Demo")

bgcolor = colors[2]
screen.fill(bgcolor)
img = pygame.image.load("invader.gif")
sound = "sound.wav"
steps = np.linspace(20, 360, 40).astype(int)

right = np.zeros((2, len(steps)))
left = np.zeros((2, len(steps)))
up = np.zeros((2, len(steps)))
down = np.zeros((2, len(steps)))

right[0] = steps
right[1] = 20
left[0] = steps[::-1]
left[1] = 360
up[0] = 20
up[1] = steps[::-1]
down[0] = 360
down[1] = steps

pos = np.concatenate((right.T, down.T, left.T, up.T))
i = 0
# pygame.draw.circle(screen, colors[0], (200, 200), 25, 0)

while True:
    screen.fill(bgcolor)
    if i%2==0:
        img = pygame.image.load("invader2.gif")
    elif i%2!=0:
        img = pygame.image.load("invader.gif")
    if i >= len(pos):
        i = 0
        # pygame.transform.rotate(img, 270)
    screen.blit(img, pos[i])
    
    text = "[step: %d, X=%d, Y=%d]" %(i, pos[i][0], pos[i][1])
    sys_font = pygame.font.SysFont("none", 19)
    rendered = sys_font.render(text, 1, colors[1])
    screen.blit(rendered, (150, 200))

    i+=1

    for e in pygame.event.get():
        if e.type == QUIT:
            play_audio(sound)
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(3)