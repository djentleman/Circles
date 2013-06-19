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
        self.nutrition = random.randint(70, 230)
        self.environment = environment
        self.eaten = False

    def getEaten(self):
        self.actualRadius -= 0.07 # one bite
        self.radius = int(self.actualRadius)
        if self.actualRadius <= 0:
            self.eaten = True
        return self.eaten

class Corpse(Food):
    def __init__(self, x, y, environment, radius):
        super().__init__(x, y, environment)
        self.radius = radius
        self.rotLevel = 0

    def rot(self):
        self.rotLevel = self.rotLevel + 0.5
        if self.rotLevel > 255:
            self.eaten = True
        return self.eaten # not actually eaten, but it will dissapear here

    def getColor(self):
        return rgb(150, int(self.rotLevel / 2), 10)

    def draw(self):
        col = self.getColor()
        pygame.draw.circle(self.environment, col,
                           (self.x, self.y), self.radius, 0)

    


class Plant(Food):
    def __init__(self, x, y, environment):
        super().__init__(x, y, environment)
        self.growthRate = (random.random() / 40)
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

class PoisonPlant(Plant):
    def __init__(self, x, y, environment):
        super().__init__(x, y, environment)
        self.toxicity = random.random() # between 0 and 1

    def getColor(self):
        #overrides super
        return rgb(int(self.toxicity * 100), 0, int(self.toxicity * 200))      
    
