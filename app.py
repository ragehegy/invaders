import pygame, sys
from pygame.locals import *
import numpy as np
import player
import game
import level

game = game.Game()
screen = game.init()
player = player.Player()

level = level.Level()
tiles = level.ground(game.width, game.height)

screen.blit(player.image, player.rect)
# screen.blit(platform.image, platform.rect)

game_text, textpos = game.game_text()
screen.blit(game_text, textpos)
sprite = pygame.sprite.RenderPlain(player)


while True:
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        quit()
    if 1 in keys:
        # if keys[K_x]:
        #     player.hit()
        player.key_move()
    else:
        player.state = "idle"
    game.clock.tick(13)
    player.rect.clamp_ip(screen.get_rect())
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == MOUSEBUTTONDOWN:
            player.hit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            # elif event.key == pygame.K_x:
            #     player.hit()
        #     elif keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
        #         player.state = "running"
        #         player.key_move()
        elif event.type == KEYUP:
            player.state = "idle"
            player.hitting = 0

    player.update()
    player.gravity(tiles)
    screen.fill(game.bgcolor)
    # draw tiles
    # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(20, 550, 960, 20), 0)
    sprite.draw(screen)
    tiles.draw(screen)
    pygame.display.flip()