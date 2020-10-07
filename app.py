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

enemy.rect.top = 450
enemy.rect.left = 600

level = level.Level()
tiles = level.ground(game.width, game.height)
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)

# screen.blit(player.image, player.rect)
# screen.blit(enemy.image, enemy.rect)
# screen.blit(platform.image, platform.rect)

game_text, textpos = game.game_text()
screen.blit(game_text, textpos)
sprite = pygame.sprite.RenderPlain(player)
wsprite = pygame.sprite.RenderPlain(widget)
# enemy_sprite = pygame.sprite.RenderPlain(enemy)


while True:
    enemy.move()
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
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_z:
                player.throw(widget)
        elif event.type == KEYUP or event.type == MOUSEBUTTONUP:
            player.state = "idle"
            player.hitting = 0
    widget_collide = pygame.sprite.spritecollide(widget, enemy_group, True)
    if widget_collide:
        widget.active = False
    collided = pygame.sprite.spritecollide(player, enemy_group, False)
    if collided:
        if player.hitting == 1:
            enemy.state == "dead"
            enemy_group.remove(collided[0])
        else:
            player.state = "dead"
    player.update()
    enemy.update()
    player.gravity(tiles)
    player.rect.clamp_ip(screen.get_rect())
    enemy.rect.clamp_ip(screen.get_rect())
    screen.fill(game.bgcolor)
    # draw tiles
    if widget.active == True:
        # screen.blit(widget.image, widget.rect)
        wsprite.draw(screen)
        widget.move()
    sprite.draw(screen)
    # enemy_sprite.draw(screen)
    tiles.draw(screen)
    enemy_group.draw(screen)
    pygame.display.flip()