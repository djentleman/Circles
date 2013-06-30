# biomes! effectivley food factories

import pygame, sys, time, random, math
from pygame.locals import *

from food import *

class Biome:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(100, 500)
        self.humidity = random.random()
        self.temprature = random.randint(2, 50) # centigrade
        self.plants = []

    def initBiome(self, environment):
        startFood = int(self.humidity * self.temprature * (self.radius / 100))
        for i in range(startFood):
            isPoison = self.humidity / 4 # 100% humid = 25% of being poison

            randX, randY = self.getFoodCoords()
            if random.random() > isPoison:
                plant = Plant(randX, randY, environment)
                plant.nutrition = abs(int((self.humidity * 10) \
                                      * (self.temprature / 2) + random.randint(-5, 5)))
            else:
                plant = PoisonPlant(randX, randY, environment)
            self.plants.append(plant)
        return self.plants

    def grow(self, playSpeed, environment):
        for plant in self.plants:
            if plant.eaten:
                self.plants.remove(plant)
                continue
            plant.grow(playSpeed)
        if random.random() > 0.98:
            randX, randY = self.getFoodCoords()
            new = Plant(randX, randY, environment)
            new.nutrition = abs(int((self.humidity * 10) * \
                             (self.temprature / 2) + random.randint(-5, 5)))
            self.plants.append(new)
        return self.plants

    def getFoodCoords(self):
        
        # random food locator is generated using natural distribution
        # with random drift
        randX = random.randint(abs(int((self.x - self.radius) ** 0.5)),
                                abs(int((self.x + self.radius) ** 0.5))) ** 2
        driftX = random.randint(-20, 20)
        randX += driftX

            
        randY = random.randint(abs(int((self.y - self.radius) ** 0.5)),
                                abs(int((self.y + self.radius) ** 0.5))) ** 2
        driftY = random.randint(-20, 20)
        randY += driftY

        return randX, randY
            
        
                
            
