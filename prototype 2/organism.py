import pygame, sys, time, random, math
from pygame.locals import *
from pygame_util import *

class Organism:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.actualX = float(x)
        self.actualY = float(y)
        self.radius = random.randint(1, 10)
        self.mass = math.pi * (self.radius * self.radius)
        self.aggressionIndex = random.randint(1, 255)
        self.aggression = float(self.aggressionIndex)
        self.environment = environment
        self.isMale = bool(random.randint(0, 1)) # 50/50 chance
        self.isFocused = False
        self.direction = random.randint(0, 360)
        self.speed = random.random() + 0.25
        self.energy = 100.0

    def focus(self):
        self.isFocused = True

    def unFocus(self):
        self.isFocused = False
        

    def draw(self):
        # get body color
        if self.isMale:
            bodyColor = rgb(0, 0, 200)
        else:
            bodyColor = rgb(255, 148, 184)
            
        pygame.draw.circle(self.environment, bodyColor,
                           (self.x, self.y), self.radius, 0)
        if not self.isFocused:        
            shellColor = rgb(self.aggressionIndex,  0, 0)
        else:
            shellColor = rgb(0, 255, 0)
        
        pygame.draw.circle(self.environment, shellColor,
                           (self.x, self.y), self.radius + 2, 2)

    def move(self):
        # make it bounce

        
        yComponent = math.sin(self.direction) * self.speed
        xComponent = math.cos(self.direction) * self.speed
        self.actualY += yComponent
        self.actualX += xComponent
        self.x = int(self.actualX)
        self.y = int(self.actualY)
