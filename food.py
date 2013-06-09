

#library imports
import time
import random
import math
from graphics import *
from threading import *


class Food:
    # food class, gets eaten when or organism touches it, and transfers
    # it's tasty nutrition
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.nutrition = random.randint(20, 150)
        self.environment = environment
        self.eaten = False
        self.radius = (random.random() * 5) + 1
        if (x < 750):
            self.body = Circle(Point(x, y), self.radius)
            self.body.setFill(color_rgb(0, self.nutrition, self.nutrition))
            self.body.draw(environment)

    # current re-sizing method inefficent

    def getEaten(self):
        self.radius -= 0.05
        self.body = Circle(Point(self.x, self.y), self.radius)
        self.body.setFill(color_rgb(0, self.nutrition, self.nutrition))
        if self.radius < 0:
            # food has died
            self.body.undraw()
            # remove from all lists
            self.eaten = True
        else:
            self.body.undraw()
            self.body.redraw(self.environment)

    def grow(self):
        self.radius += 0.05
        self.body = Circle(Point(self.x, self.y), self.radius)
        self.body.setFill(color_rgb(0, self.nutrition, self.nutrition))
        self.body.undraw()
        self.body.draw(self.environment)
