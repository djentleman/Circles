# food
import pygame, sys, time, random, math
from pygame.locals import *

from pygame_util import *

class Food:
    # corpse and plant inherit from food
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.radius = random.randint(1, 6)
        self.actualRadius = float(self.radius)
        self.nutrition = random.randint(100, 200)
        self.environment = environment

    def getEaten(self):
        self.actualRadius -= 0.07 # one bite
        self.radius = int(self.actualRadius)


class Plant(Food):
    def __init__(self, x, y, environment):
        super().__init__(x, y, environment)
        self.growthRate = (random.random() / 10)
        # rate at which the organism grows

    def grow(self):
        self.actualRadius += self.growthRate
        self.radius = int(self.actualRadius)
    
    def getColor(self):
        return rgb(0, self.nutrition, 0)

    def draw(self):
        col = self.getColor()
        pygame.draw.circle(self.environment, col,
                           (self.x, self.y), self.radius, 0)
    
