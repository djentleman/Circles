

#library imports
import time
import random
import math
from graphics import *
from threading import *


class Food:
    # food class, gets eaten when or organism touches it, and transfers
    # it's tasty nutrition
    def __init__(self, x, y, nutrition, environment):
        self.x = x
        self.y = y
        self.nutrition = nutrition
        self.environment = environment
        self.eaten = False
        self.body = Point(x, y)
        self.body.setFill(color_rgb(0, nutrition, nutrition))
        self.body.draw(environment)

    def getEaten(self):
        self.body.undraw()
        #remove from any lists

class FoodCluster:
    # foodSource generates lots of food from set coords
    def __init__(self, x, y, environment):
        self.maxSpread = random.randint(3, 35) # radius of spread
        self.x = x
        self.y = y
        self.environment = environment
        self.nutrition = random.randint(20, 150)


    def generateCluster(self):
        # generate an initial cluster of food around x and y
        allFood = []
        initFood = random.randint(1, 5)
        for i in range(initFood):
            food = self.generateFood()
            allFood.append(food)
        return allFood # returns array of food

    def generateFood(self):
        # generates one piece of food in the cluster
        spreadX = random.randint(-self.maxSpread, self.maxSpread)
        spreadY = random.randint(-self.maxSpread, self.maxSpread)
        food = Food(self.x + spreadX, self.y + spreadY, self.nutrition, self.environment)
        # initing food draws it
        return food # returns the food
