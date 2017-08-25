#!/usr/bin/env python
# coding: utf-8
# author: YYY <ldh@qq.com>
import pygame
from pygame.locals import *
import time
import random

# 分数统计
score=0
miss=0

# 主战机
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        # self.surf = pygame.Surface((25,25))
        # self.surf.fill((255,255,255))
        self.image = pygame.image.load('warcraft.png').convert_alpha()
        self.image.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.image.get_rect()
        self.speed = 10

    def update(self,press_keys):
        if press_keys[K_UP]:
            self.rect.move_ip(0,-self.speed)
        if press_keys[K_DOWN]:
            self.rect.move_ip(0,self.speed)
        if press_keys[K_LEFT]:
            self.rect.move_ip(-self.speed,0)
        if press_keys[K_RIGHT]:
            self.rect.move_ip(self.speed,0)

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

# 敌机
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.image.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.image.get_rect(center=(
            random.randint(20,780),0
        ))
        self.speed = random.randint(2,12)
        if random.randint(0,1) == 0:
            if self.rect.right > 400:
                self.forward = -2
            else: 
                self.forward = 2
        else:
            self.forward = 0
    
    def update(self):
        self.rect.move_ip(self.forward, self.speed)
        # if self.rect.bottom > 600:
        #     self.kill()
        #
    # def kill(self):
    #     super(self.kill)
    #     self.image = pygame.image.load('boom.png').convert_alpha()
    #     self.image.set_colorkey((255,255,255),RLEACCEL)

# 子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet,self).__init__()
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.image.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top <0:
            self.kill()

# 炸弹
class Boom(pygame.sprite.Sprite):
    def __init__(self):
        super(Boom,self).__init__()
        self.image = pygame.image.load('boom2.png').convert_alpha()
        self.image.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.image.get_rect(
            center=(
                random.randint(0,800),random.randint(0,300)
            )
        )

    def update(self):
        self.rect.move_ip(0,1)
        if self.rect.bottom > 600:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('HitPlane')
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDBULLET = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBULLET,50)
player = Player()
player.rect.bottom = 600
player.rect.right = 400
clock = pygame.time.Clock()
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
booms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
running = True
aliving = True


def draw_text(mytext,posx,posy):
    fontObj = pygame.font.Font('Oreos.ttf', 16)
    textSurfaceObj = fontObj.render(mytext, True, (255, 255, 255))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (posx, posy)
    screen.blit(textSurfaceObj, textRectObj)

while running:
    clock.tick(50)
    # drawText('score：',20,20)
    if not aliving:
        choice = input("Press any keys to quit.")
        exit()
    if aliving:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                if random.randint(0,50)==1:
                    new_boom = Boom()
                    booms.add(new_boom)
                    all_sprites.add(new_boom)
            elif event.type == ADDBULLET:
                new_bullet = Bullet()
                new_bullet.rect.bottom = player.rect.bottom - 30
                new_bullet.rect.right = player.rect.right - 28
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)                
        # draw
        screen.blit(background, (0, 0))
        press_keys = pygame.key.get_pressed()
        player.update(press_keys)
        enemies.update()
        bullets.update()
        booms.update()
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # 检测碰撞
        # pygame.sprite.spritecollide(player, enemies,True)
        if pygame.sprite.spritecollideany(player,enemies):
            player.kill()
            aliving = False
        for my_bullet in bullets:
            die_enemies = pygame.sprite.spritecollide(my_bullet,enemies,True)
            if die_enemies:
                score += len(die_enemies)
        if booms:
            if pygame.sprite.spritecollide(player,booms,True):
                score += len(enemies)
                for enemie in enemies:
                    enemie.kill()
        for enemie in enemies:
            if enemie.rect.bottom > 600:
                miss += 1
                enemie.kill()

        draw_text('Score:{score}'.format(score=score),60,20)
        draw_text('Miss:{miss}'.format(miss=miss), 74,50)
        pygame.display.update()
        # pygame.display.flip()
        # time.sleep(0.02)