import pygame
import sys
import os
from util import *
import player
import Platform
from random import randint


class main:
    def __init__(self, width=500, height=500):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "450,30"
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height+100))
        self.Clock = pygame.time.Clock()
        self.player = player.Player()
        self.reset()
        self.lava = pygame.Rect(0, height - 30, width, 30)
        pygame.mixer.music.load('8bit.mp3')
        pygame.mixer.music.play(-1)

    def reset(self):
        self.timeLeft = 120
        self.Platforms = []
        self.Platforms.append(Platform.Platform(self.width, 5))
        self.player.Speed = [0,0]
        self.player.point = 0
        self.player.sound()
        self.player.PlayerRect.y = 1
        self.player.windTime = randint(1800, 3600)
        self.player.PlayerRect.centerx = self.Platforms[0].platform.centerx
        self.Platforms[0].platform.y = 40

    def run(self):
        while True:
            self.draw()
            self.player.move()
            self.handleInput()
            self.PlatCollision()
            self.MovePlat()
            self.PlatDispawn()
            self.spawnPlatform()
            self.mapCollision()

    def DrawMap(self):
        pygame.draw.rect(self.screen, RGB("#d73900ff"), self.lava)
        pygame.draw.rect(self.screen, RGB("#0a0083ff"), (0, self.height, self.width, 100))

    def draw(self):
        self.screen.fill((20, 20, 20))
        self.player.DrawPlayer(self.screen)
        self.DrawPlat()
        self.player.indicator()
        self.DrawMap()
        pygame.display.flip()

    def mapCollision(self):
        if self.player.PlayerRect.y > self.width + 20:
            self.reset()
        elif self.player.PlayerRect.left < 0:
            self.player.Speed[0] *= -0.5
            self.player.PlayerRect.x = 3
        elif self.player.PlayerRect.right > self.width:
            self.player.Speed[0] *= -0.5
            self.player.PlayerRect.right = self.width - 3
        elif self.player.PlayerRect.top < 0:
            self.player.Speed[1] = 0
            self.player.PlayerRect.top = 1

    def handleInput(self):
        self.Clock.tick(60)
        self.event = pygame.event.get()
        for event in self.event:
            if event.type == pygame.QUIT:
                sys.exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.pos[1] < self.height + 100 and event.pos[1] > self.hegiht
            #         if event.pos[0] < self.width / 2 and event.pos[0] > self.width
            #             pass
        self.player.HandelInput(self.event)

    def spawnPlatform(self):
        if self.timeLeft < 1:
            self.player.point += 1
            self.Platforms.append(Platform.Platform(self.width,5))
            if self.Platforms[-1].platformtype == 1:
                self.timeLeft = 300
            else:
                self.timeLeft = 120
            print(self.player.point)
        self.timeLeft -= 1

    def PlatCollision(self):
        for x in self.Platforms:
            x.collide(self.player)

    def DrawPlat(self):
        for x in self.Platforms:
            x.DrawPlatform(self.screen)

    def MovePlat(self):
        for x in self.Platforms:
            x.move()

    def PlatDispawn(self):
        if self.Platforms[0].platform.y >= self.width + 40:
            self.Platforms.pop(0)

run = main(500,550)
run.run()
