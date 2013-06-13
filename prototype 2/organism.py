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

        self.sightRays = 10 # number of rays in sight
        self.sightRange = 40 # range of each ray
        self.sightWidth = 60 # how wide the vision is in degrees

        # keen vision: lots of rays with a small width - probably high depth
        # unkeen: less dense ray population over a large area, probably low depth

    def focus(self):
        self.isFocused = True

    def traceRay(self, direction):
        # traces one ray, and retuens the color found in that direction
        # white is invisible
        # append this color to an array - get a circle eyed view of the world
        # direction = direction ray is traveling
        # actual direction = direction + self.direction

        # trif is done in radians - fix this!
        rayDirection = ((math.pi * self.direction) / 180) + ((math.pi * direction) / 180)
        rayX = self.actualX
        rayY = self.actualY
        for i in range(self.sightRange):
            try:
                # range is measured in pixels
                rayX += math.cos(rayDirection)
                rayY += math.sin(rayDirection)
                # print(rayX, rayY)
                color = self.environment.get_at((int(rayX), int(rayY)))
                if color != (0, 0, 0, 255) and color != (255, 255, 255, 255):
                    return color # seen something
                if self.isFocused:
                    # show tracing path
                    self.environment.set_at((int(rayX), int(rayY)), rgb(0, 255, 0))
            except (Exception):
                # out of bounds error
                return rgb(255, 255, 255) # wall!
        return rgb(0, 0, 0) # black
            
        
        

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
                           (self.x, self.y), self.radius + 1, 2)

    def move(self, playSpeed):
        speed = self.speed * playSpeed
        direction = (math.pi * self.direction) / 180

        yComponent = math.sin(direction) * speed
        xComponent = math.cos(direction) * speed
        #wall collision detection goes here
        self.actualY += yComponent
        self.actualX += xComponent
        self.x = int(self.actualX)
        self.y = int(self.actualY)
