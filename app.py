import pygame, sys
from pygame.locals import *
import numpy as np
import player
import game
import level

game = game.Game()
screen = game.init()
player = player.Player()

# level = level.Level()
# level.rect.top = game.height - level.rect.size[0]

screen.blit(player.image, player.rect)
# screen.blit(level.image, level.rect)

game_text, textpos = game.game_text()
screen.blit(game_text, textpos)
sprite = pygame.sprite.RenderPlain(player)
# lvl_sprite = pygame.sprite.RenderPlain(level)


while True:
    keys = pygame.key.get_pressed()
    if 1 in keys:
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
        # elif event.type == KEYDOWN:
        #     if keys[pygame.K_SPACE]:
        #         player.state = "jumping"
        #         player.jump()
        #     elif keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
        #         player.state = "running"
        #         player.key_move()
        elif event.type == KEYUP:
            player.state = "idle"
            player.jumpCount = 20

    player.update()
    # player.gravity()
    screen.fill(game.bgcolor)
    # draw tiles
    # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(20, 550, 960, 20), 0)
    sprite.draw(screen)
    # lvl_sprite.draw(screen)
    pygame.display.flip()