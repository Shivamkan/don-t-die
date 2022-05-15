from util import *
import pygame
from random import randint


class Platform:
    def __init__(self, width, speed):
        self.platform = pygame.Rect(randint(0, 10)* (width/15),-20, 200, 40)
        self.speed = speed
        self.platformtype = randint(0,10)
        self.land = pygame.mixer.Sound("land.wav")

    def move(self):
        self.platform.y += self.speed / 5
        # print(self.platform.y,"platform y")

    def DrawPlatform(self, screen, color="#833d13ff"):
        if self.platformtype != 1:
            pygame.draw.rect(screen, (RGB(color)), self.platform)
        else:
            pygame.draw.rect(screen, (RGB('#00ff00')), self.platform)

    def collide(self, player):
        ColliedTolerance = 10
        if player.PlayerRect.colliderect(self.platform):
            if abs(self.platform.right - player.PlayerRect.left) <= ColliedTolerance:
                player.Speed[0] = 0
                player.Speed[1] *= 0.3
                player.PlayerRect.x += 5
            elif abs(self.platform.left - player.PlayerRect.right) <= ColliedTolerance:
                player.Speed[0] = 0
                player.Speed[1] *= 0.3
                player.PlayerRect.x -= 5
            if abs(self.platform.top - player.PlayerRect.bottom) <= ColliedTolerance:
                if self.platformtype != 1:
                    if player.Speed[1] > 4:
                        pygame.mixer.Sound.play(self.land)
                    player.Speed[1] = 0
                    player.Speed[0] = 0
                    if player.parachute == 1:
                        player.Gravity *= 2
                        player.parachute = 0
                elif self.platformtype == 1:
                    player.Speed[1] = -15
                    player.Speed[0] = 0
                    if player.parachute == 0:
                        player.Gravity /= 2
                        player.parachute = 1
            elif abs(self.platform.bottom - player.PlayerRect.top) <= ColliedTolerance + 5:
                player.Speed[1] *= -0.5
                player.PlayerRect.y += 10