import pygame, sys, time, random, math
from pygame.locals import *
from pygame_util import *
from genetics import *
from food import *




class Organism:
    def __init__(self, x, y, environment):
        self.genes = generateGenes()
        self.genome = generateRandomChromosome(self.genes)
        # THIS NEEDS TO BE SORTED IN THE GOM!^
        self.x = x
        self.y = y
        self.actualX = float(x)
        self.actualY = float(y)
        self.scrollX = x
        self.scrollY = y
        self.radius = random.randint(3, 10)
        self.naturalRadius = self.radius # this size when healthy
        self.actualRadius = float(self.radius)
        self.mass = math.pi * (self.radius * self.radius)
        self.aggressionIndex = random.randint(1, 255)
        self.aggression = float(self.aggressionIndex)
        self.environment = environment
        self.isMale = bool(random.randint(0, 1)) # 50/50 chance
        self.isFocused = False
        self.direction = random.randint(0, 360)
        self.speed = 1
        self.naturalSpeed = self.speed
        self.kenisisTimer = 0
        self.energy = 100.0
        self.alive = True

        self.sightRays = random.randint(5, 12)# number of rays in sight
        if self.sightRays % 2 == 0:
            self.sightRays += 1
        self.sightRange = random.randint(20, 80) # range of each ray
        self.sightWidth = random.randint(4, 12) ** 2
        # how wide the vision is in degrees
        self.vision = []

        # keen vision: lots of rays with a small width - probably high depth
        # unkeen: less dense ray population over a large area, probably low depth
        self.behavior = "Taxis"
        self.eating = None # once something is being eaten it becomes
        # an attribute temporarily
        # stops messy O(n^2) algorithms

        self.poisoned = False # poisoning damages energy heavily

        self.nerveDensity = random.randint(4, 10)

        self.setUpGenetics()

    def setUpGenetics(self):
        for gene in range(len(self.genome.genome)):
            
            #for effect in range(len(self.chromosome.getGene(gene))):
            #alleles need to be an attribue of genes
            #print(self.genome.genome)
            thisGene = self.genome.getGene(gene)
            if thisGene[0] == 1 or thisGene[1] == 1:
                #AA, Aa, aA
               
                for effect in (self.genes[gene].phenotype):
                    if(effect == "spdcf"):
                        self.speed *= 0.9
                        self.naturalSpeed = self.speed
                    elif(effect == "spdcn"):
                        self.speed += 0.4
                        self.naturalSpeed = self.speed
            else:
                for effect in (self.genes[gene].phenotype):
                    if(effect == "spdcf"):
                        self.speed *=  0.5
                        self.naturalSpeed = self.speed
            #print(self.speed)
    
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

        rayDirection = ((math.pi * self.direction) / 180) + ((math.pi * direction) / 180)
        rayX = self.scrollX + ((self.radius + 3) * math.cos(rayDirection))
        rayY = self.scrollY + ((self.radius + 3) * math.sin(rayDirection))
        for i in range(self.sightRange):
            if (rayX > 650 and self.actualX > 1900) or (rayX < 0 and self.actualX < 100) \
               or (rayY > 650 and self.actualY > 1900) or (rayY < 0 and self.actualY < 100):
                return rgb(255, 255, 255)
            try:
                # range is measured in pixels
                # print(rayX, rayY)
                color = self.environment.get_at((int(rayX), int(rayY)))
                if color != (0, 0, 0, 255) \
                   and color != (0, 255, 0, 255) and color != self.getBodyColor() \
                   and rayX < 650:
                    return color # seen something
                if self.isFocused:
                    # show tracing path
                    self.environment.set_at((int(rayX), int(rayY)), rgb(0, 255, 0))
                rayX += math.cos(rayDirection)
                rayY += math.sin(rayDirection)
            except (Exception):
                # out of bounds error
                return rgb(0, 0, 0) # wall!
        return rgb(0, 0, 0) # black

    def turn(self, change):
        self.direction += change
        self.direction = (self.direction % 360)

    def accelerate(self, change):
        self.speed += change
        
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
        
    
    def draw(self, scrollX, scrollY):
        self.scrollX = int(self.x - scrollX)
        self.scrollY = int(self.y - scrollY)
        bodyColor = self.getBodyColor()
            
        pygame.draw.circle(self.environment, bodyColor,
                           (self.scrollX, self.scrollY),
                           self.radius, 0)
        if not self.isFocused:        
            shellColor = rgb(self.aggressionIndex,  20, 20)
        else:
            shellColor = rgb(0, 255, 0)
        
        pygame.draw.circle(self.environment, shellColor,
                           (self.scrollX, self.scrollY),
                            self.radius + 1, 2)

    def wander(self, playSpeed):
        speed = self.speed * playSpeed
        # energy (kinetic) can be measured by (mv^2)/2
        # but that would sap too much, so well use a multiplyer, η
        # e(w) = (η(πr^2)v^2)/2 = (ηmv^2)/2
        energyToSap = (0.003 * self.mass * (self.speed * self.speed)) / 2
        # η is taken as 0.003

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

    def analysePixel(self, pixel):
        # returns either: True (move towards)
        # False (move away) or None (neither)

        if pixel == rgb(255, 255, 255):
            return False # walls
        
        if pixel[1] == pixel[2] and pixel[0] < self.aggression + 30 \
           and pixel != rgb(0, 0, 0):
            self.behavior = "Chase"
            return True # flocking
        elif pixel[1] == pixel[2] and pixel[0] >= self.aggression + 30 \
           and pixel != rgb(0, 0, 0):
            if pixel[0] > self.aggression + 60:
                self.behavior = "Kenisis"
            return False # running
        
        if pixel[0] == 10 and pixel[2] == 10:
            # plant
            return True # food
        if self.behavior == "Chase":
            self.behavior = "Taxis"
        
        
        return None
        

    def taxis(self):
        # this is an unintellegent version, presents some bugs
        
        # vision = self.vision
        if len(self.vision) % 2 == 1:
            centre = int(len(self.vision) / 2)
        else:
            centre = int(len(self.vision) / 2) - 1
        centrePixel = self.analysePixel(self.vision[centre])
        if centrePixel != None and self.vision[centre] != rgb(255, 255, 255):
            if centrePixel:
                return 0
            else:
                return 1
        
        half = int(len(self.vision) / 2) # odd number is half - 0.5
        for index in range(0, half):
            # scan left half of vision
            pixelAnalysis = self.analysePixel(self.vision[index])
            if pixelAnalysis != None:
                if pixelAnalysis: # true
                    return -1.5
                return 1.5
            pixelAnalysis = self.analysePixel(self.vision[-(index + 1)])
            if pixelAnalysis != None:
                if pixelAnalysis: # true
                    return 1.5
                return -1.5
        return 0

    def checkForThreat(self, pixel):
        if pixel[1] == pixel[2] and pixel[0] > self.aggression + 50 \
           and pixel[1] != 255:
            return True
        return False

    def kenisis(self):
        safe = True
        for pixel in self.vision:
            if self.checkForThreat(pixel):
                #threat detected
                self.kenisisTimer = 40
                safe = False
        if safe:
            self.kenisisTimer -= 1
        if self.kenisisTimer == 0:
            self.behavior = "Taxis"
        if random.random() > 0.8:
            return random.randint(-5, 5)
        else:
            return 0
                
    def touch(self):
        #checks if pixel is directly touching self
        # direction is in degrees
        direction = 0
        gap = 360 / self.nerveDensity
        while direction <= 360:
            if direction > 360:
                break
            try:
                touchDirection = (math.radians(self.direction) + math.radians(direction)) % 360
                for sensitivity in range(3, 5):
                    currentPixelX = (math.cos(touchDirection) * (self.radius + sensitivity)) + self.scrollX
                    currentPixelY = (math.sin(touchDirection) * (self.radius + sensitivity)) + self.scrollY
                    pixel = self.environment.get_at((int(currentPixelX), int(currentPixelY)))
                    if not pixel == rgb(0, 0, 0) and not pixel == rgb(0, 255, 0):
                        if direction < (self.sightWidth / 2) or direction > (360 - (self.sightWidth / 2)):
                            return True # see and touch
                        else:
                            return False # only touch
            except (Exception):
                x = 1# lol
            direction += gap
        return None # not touching anything
        
        

    

    def move(self, playSpeed, potentialFood):
        energyToSap = 0
        organisms = potentialFood[0]
        corpses = potentialFood[1]
        plants = potentialFood[2]
        
        # one movement

        # seeing goes here
        self.vision = self.look()
        touching = self.touch()

        if touching != None: # second statement may need to change
            # touching something!
            if touching:
                # check for food
                foundFood = False
                for plant in plants:
                    if (plant.x + plant.actualRadius) > (self.actualX - self.actualRadius) and \
                       (plant.x - plant.actualRadius) < (self.actualX + self.actualRadius) and \
                       (plant.y + plant.actualRadius) > (self.actualY - self.actualRadius) and \
                       (plant.y - plant.actualRadius) < (self.actualY + self.actualRadius):
                        self.behavior = "Eating"
                        self.eating = plant
                        foundFood = True
                        break
                if not foundFood:
                    self.eating = None
                    self.behavior = "Taxis"
                    # check for mate
                    foundMate = False
                    for organism in organisms:
                        if (organism.actualX + organism.actualRadius) > (self.actualX - self.actualRadius) and \
                           (organism.actualX - organism.actualRadius) < (self.actualX + self.actualRadius) and \
                           (organism.actualY + organism.actualRadius) > (self.actualY - self.actualRadius) and \
                           (organism.actualY - organism.actualRadius) < (self.actualY + self.actualRadius):
                            if organism.isMale != self.isMale:
                                # opposite secks
                                self.behavior = "MATING"
                                foundMate = True
                                childGenome = breed(organism.genome, self.genome)
                                print(organism.genome.genome)
                                print(self.genome.genome)
                                print(childGenome)
                                print()
                                break
                    if not foundMate:
                        self.eating = None
                        self.behavior = "Taxis"
                          
                
 
            else:
                # dont know what it is, shit yourself!
                x = 1
                
        
        if self.behavior == "Taxis":
            if self.speed > self.naturalSpeed:
                self.accelerate(-self.speed * 0.04)
            elif self.speed < self.naturalSpeed:
                self.speed = self.naturalSpeed
                
            change = self.taxis() * playSpeed
            self.turn(change)
            
        elif self.behavior == "Kenisis":
            if self.speed < self.naturalSpeed * 1.7:
                self.accelerate(self.speed * 0.04)
                
            change = self.kenisis()
            self.turn(change)

        elif self.behavior == "Eating":
            if self.eating != None:
                energyToSap -= self.eating.nutrition / 150
                if self.eating.getEaten(playSpeed):
                    # fully eaten
                    try:
                        potentialFood[2].remove(self.eating)
                    except (Exception):
                        x = 1
                    self.eating = None
                    self.behavior = "Taxis"
        elif self.behavior == "Chase":
            self.accelerate(0.1)

        else:
            self.behavior = "Taxis"

                        
            
            
        
        # thinking goes here, analyse vision
        if not self.behavior == "Eating":
            energyToSap += self.wander(playSpeed)

                

        if energyToSap != 0:
            self.energy -= (energyToSap * playSpeed)
            if self.speed == 0:
                self.speed = self.naturalSpeed
        else:
            #idle, only 'warm bloods'
            self.speed = 0
            self.energy -= (0.001 * playSpeed)

        if self.energy < 0:
            self.die()

        self.actualRadius -= (energyToSap / 10) * playSpeed
            
        if self.actualRadius < 2:
            self.actualRadius = 2.0
        self.radius = int(self.actualRadius)

        self.mass = math.pi * (self.actualRadius * self.actualRadius)
        

        return self.alive, potentialFood
            

        
