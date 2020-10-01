import pygame, sys
from pygame.locals import *
import numpy as np
import player
import game

game = game.Game()
screen = game.init()
player = player.Player()
screen.blit(player.image, player.rect)
game_text, textpos = game.game_text()
screen.blit(game_text, textpos)
sprite = pygame.sprite.RenderPlain(player)


while True:
    game.clock.tick(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            player.hit()
        elif event.type == KEYDOWN:
            player.key_move()

    sprite.update()
    screen.fill(game.bgcolor)
    # screen.blit(coin.image, coin.rect)
    sprite.draw(screen)
    pygame.display.flip()