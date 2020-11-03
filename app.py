import pygame, sys
from pygame.locals import *
import numpy as np
import player
import game
import level
import enemy
import widget

game = game.Game()
screen = game.init()
player = player.Player()
enemy = enemy.Enemy()
widget = widget.Widget()

enemy.rect.top = 650
enemy.rect.left = 600

level = level.Level(game.dimensions[0], game.dimensions[1])
lvl_tiles = level.build()
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)

game_text, textpos = game.game_text()
screen.blit(game_text, textpos)
sprite = pygame.sprite.RenderPlain(player)
wsprite = pygame.sprite.RenderPlain(widget)

while True:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if keys[K_ESCAPE]:
        quit()
    if 1 in keys or 1 in mouse:
        player.key_move()
    else:
        player.state = "idle"
    game.clock.tick(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN:
            # if event.key == pygame.K_SPACE:
            #     player.jump()
            if event.key == pygame.K_z:
                player.throw(widget)
        elif event.type == KEYUP or event.type == MOUSEBUTTONUP:
            player.state = "idle"
            player.hitting = 0
            if event.key == pygame.K_SPACE:
                player.jumpCount = 6

    # collisions
    widget_collide = pygame.sprite.spritecollide(widget, enemy_group, True, pygame.sprite.collide_mask )
    if widget_collide:
        widget.active = False
    collided = pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_mask )
    if collided:
        if player.hitting == 1:
            enemy.state == "dead"
            enemy_group.remove(collided[0])
        else:
            player.state = "dead"

    player.update(lvl_tiles)
    player.rect.clamp_ip(screen.get_rect())
    enemy.update()
    enemy.rect.clamp_ip(screen.get_rect())

    # screen.fill(game.bgcolor)
    screen.blit(game.bgimg, (0,0))
    if widget.active == True:
        wsprite.draw(screen)
        widget.move()
    enemy.move()
    sprite.draw(screen)
    lvl_tiles.draw(screen)
    enemy_group.draw(screen)
    screen.blit(game_text, textpos)
    pygame.display.flip()