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
    
    # print(">>>>>>>>>>>")
    # print("start here")
    # count = 0
    # count+=1
    # print("count: {}".format(count))
    
    key_pressed = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    
    if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
        player.direction["bottom"] = 1
    if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
        player.direction["top"] = 1
    if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
        player.direction["left"] = 1
    if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
        player.direction["right"] = 1
    if key_pressed[pygame.K_SPACE]:
        player.jump()
    if key_pressed[pygame.K_x] or mouse[0]:
        player.hit()
    if not key_pressed:
        player.state = "idle"
    if key_pressed[K_ESCAPE]:
        quit()
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_z:
                player.throw(widget)
        else:
            if event.type == KEYUP:
                player.state = "idle"
                player.hitting = 0
                if event.key == pygame.K_SPACE:
                    player.jumpCount = 6
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    player.state = "idle"
                    player.hitting = 0

    enemy.update()
    enemy.rect.clamp_ip(screen.get_rect())
    enemy.move()

    screen.blit(game.bgimg, (0,0))
    lvl_tiles.draw(screen)
    
    player.update(lvl_tiles)
    player.rect.clamp_ip(screen.get_rect())
    sprite.draw(screen)
    enemy_group.draw(screen)
    screen.blit(game_text, textpos)

    hit_list = []
    for tile in lvl_tiles:
        if player.rect.colliderect(tile):
            # hit_list.append(tile)
            clip = player.rect.clip(tile.rect)
            pygame.draw.rect(screen, pygame.Color('red'), clip)
            print("clip: {}, {}".format(clip.bottom, clip.top))
    # hit_list = pygame.sprite.spritecollide(player, lvl_tiles, False )

    # collisions
    widget_collide = pygame.sprite.spritecollide(widget, enemy_group, True )
    if widget_collide:
        widget.active = False
    collided = pygame.sprite.spritecollide(player, enemy_group, False)
    if collided:
        if player.hitting == 1:
            enemy.state == "dead"
            enemy_group.remove(collided[0])
        else:
            player.state = "dead"

    # screen.fill(game.bgcolor)
    if widget.active == True:
        wsprite.draw(screen)
        widget.move()

    pygame.display.flip()
    
    game.clock.tick(20)