import pygame
from util import *
from random import randint

class Player:
    def __init__(self, Gravity=10, airFricton=5):
        self.Gravity = Gravity
        self.fricton = airFricton
        self.Speed = [0, 0]
        self.point = 0
        self.dragstate = 0
        self.parachute = 0
        self.PlayerRect = pygame.Rect(250, -50, 30, 30)
        self.windTime = randint(1800, 3600)
        self.windSound = pygame.mixer.Sound("wind.wav")

    def move(self):
        if self.windTime >= 0:
            self.windTime -= 1
        # print(self.windTime)
        self.Speed[1] += self.Gravity / 100
        self.PlayerRect.y += round(self.Speed[1])
        if self.Speed[0] <= -0.5:
            self.Speed[0] += self.fricton / 500
        elif self.Speed[0] >= 0.5:
            self.Speed[0] -= self.fricton / 500
        else:
            self.Speed[0] = 0
        self.PlayerRect.x += round(self.Speed[0])
        if self.windTime == 0:
            self.windLeft = 600
            self.windSpeed = randint(-10, 10)/15
            self.windTime = -1
            pygame.mixer.Sound.play(self.windSound)
        elif self.windTime == -1:
            if self.windLeft > 0:
                self.Speed[0] += self.windSpeed
                self.windLeft -= 1
            else:
                self.windTime = randint(1800, 3600)
                pygame.mixer.Sound.stop(self.windSound)

    def sound(self):
        pygame.mixer.Sound.stop(self.windSound)

    def DrawPlayer(self, screen, color="#00c693ff"):
        self.screen = screen
        pygame.draw.rect(self.screen, (RGB(color)), self.PlayerRect)

    def HandelInput(self, Input):
        for event in Input:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dragstate = 1
                self.startdrag = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                self.enddrag = event.pos
                self.dragstate = 2
                self.addSpeed()

    def addSpeed(self):
        if abs(self.Speed[0]) <= 1 or self.parachute == 1 :
            Speed = listsub(self.startdrag, self.enddrag)
            Speed = [clamp(Speed[0], -120, 120), clamp(Speed[1], -120, 120)]
            self.Speed = listdivied(Speed, -10)
            self.dragstate = 0



    def indicator(self):
        if self.dragstate == 1:
            y = listsub(self.startdrag, pygame.mouse.get_pos())
            y = listdivied(y, -1)
            pygame.draw.line(self.screen, (RGB("#ff000fff")), self.PlayerRect.center,
                             listadd(self.PlayerRect.center, y), 5)
