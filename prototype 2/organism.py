import pygame, sys, time, random, math
from pygame.locals import *
from pygame_util import *
from food import *

class Organism:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.actualX = float(x)
        self.actualY = float(y)
        self.radius = random.randint(1, 10)
        self.actualRadius = float(self.radius)
        self.mass = math.pi * (self.radius * self.radius)
        self.aggressionIndex = random.randint(1, 255)
        self.aggression = float(self.aggressionIndex)
        self.environment = environment
        self.isMale = bool(random.randint(0, 1)) # 50/50 chance
        self.isFocused = False
        self.direction = random.randint(0, 360)
        self.speed = random.random() + 0.25
        self.energy = 100.0
        self.alive = True

        self.sightRays = random.randint(5, 15) # number of rays in sight
        self.sightRange = random.randint(20, 80) # range of each ray
        self.sightWidth = random.randint(30, 100) # how wide the vision is in degrees
        self.vision = []

        # keen vision: lots of rays with a small width - probably high depth
        # unkeen: less dense ray population over a large area, probably low depth
        self.action = "wander"
        self.eating = None # once something is being eaten it becomes
        # an attribute temporarily
        # stops messy O(n^2) algorithms

        self.poisoned = False # poisoning damages energy heavily


    def focus(self):
        self.isFocused = True

    def unFocus(self):
        self.isFocused = False

    def look(self):
        #work out the gap - the number of degrees between each ray
        #gap = total degrees / (number of rays - 1)
        gap = self.sightWidth / (self.sightRays - 1)
        gap = int(gap)
        vision = []
        for direction in range(int(-(self.sightWidth / 2)), int(self.sightWidth / 2), gap):
            vision.append(self.traceRay(direction))
        #print(vision)
        return vision
        

    def traceRay(self, direction):
        # add possible range detection
        # if something is close enough then i will eat/mate
        
        # traces one ray, and retuens the color found in that direction
        # white is invisible
        # append this color to an array - get a circle eyed view of the world
        # direction = direction ray is traveling
        # actual direction = direction + self.direction

        # trif is done in radians - fix this!
        rayDirection = ((math.pi * self.direction) / 180) + ((math.pi * direction) / 180)
        rayX = self.actualX + (self.radius * math.cos(rayDirection))
        rayY = self.actualY + (self.radius * math.sin(rayDirection))
        for i in range(self.sightRange):
            try:
                # range is measured in pixels
                # print(rayX, rayY)
                color = self.environment.get_at((int(rayX), int(rayY)))
                if color != (0, 0, 0, 255) and color != (255, 255, 255, 255) \
                   and color != (0, 255, 0, 255) and color != self.getBodyColor():
                    return color # seen something
                if self.isFocused:
                    # show tracing path
                    self.environment.set_at((int(rayX), int(rayY)), rgb(0, 255, 0))
                rayX += math.cos(rayDirection)
                rayY += math.sin(rayDirection)
            except (Exception):
                # out of bounds error
                return rgb(255, 255, 255) # wall!
        return rgb(0, 0, 0) # black
            
        
    def die(self):
        self.alive = False

    def getCorpse(self):
        corpse = Corpse(self.x, self.y, self.environment, self.radius)
        return corpse

        
    def getBodyColor(self):
        # get body color
        if self.isMale:
            return rgb(0, 0, 200)
        else:
            return rgb(255, 148, 184)
        
    
    def draw(self):
        bodyColor = self.getBodyColor()
            
        pygame.draw.circle(self.environment, bodyColor,
                           (self.x, self.y), self.radius, 0)
        if not self.isFocused:        
            shellColor = rgb(self.aggressionIndex,  0, 0)
        else:
            shellColor = rgb(0, 255, 0)
        
        pygame.draw.circle(self.environment, shellColor,
                           (self.x, self.y), self.radius + 1, 2)

    def wander(self, playSpeed):
        speed = self.speed * playSpeed
        # energy (kinetic) can be measured by (mv^2)/2
        # but that would sap too much, so well use a multiplyer, η
        # e(w) = (η(πr^2)v^2)/2 = (ηmv^2)/2
        energyToSap = (0.005 * self.mass * (self.speed * self.speed)) / 2
        # η is taken as 0.005

        if self.energy > energyToSap:
            # can sap
            
            direction = (math.pi * self.direction) / 180

            yComponent = math.sin(direction) * speed
            xComponent = math.cos(direction) * speed
            #wall collision detection goes here
            self.actualY += yComponent
            self.actualX += xComponent
            self.x = int(self.actualX)
            self.y = int(self.actualY)

            # return energy loss
            return energyToSap
        return 0

    def move(self, playSpeed):
        
        # one movement

        # seeing goes here
        self.vision = self.look()
        

        # thinking goes here, analyse vision

        energyToSap = self.wander(playSpeed)

        if energyToSap != 0:
            self.energy -= (energyToSap * playSpeed)
        else:
            #idle
            self.energy -= (0.005 * playSpeed)

        if self.energy < 0:
            self.die()

        return self.alive
            

        
