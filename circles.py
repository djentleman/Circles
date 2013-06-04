## Todd And Daves 'Circles'

import time
import random
import math
from graphics import *
from threading import *

s = Semaphore() # implements mutal exclusion
speedMult = 1 # speed multiplier - global (for now)

class Organism:
    # circle class - the digital organism itself
    # phenotypes are attributes, eg: speed, vision...
    # ultimatley each organism will be running on a seperate thread
    def __init__(self, spawn, environment):
        self.spawn = spawn
        self.body = Circle(spawn, random.random() * 6) # radius is random from now
        self.alive = True # turns false when dead
        self.environment = environment

        self.speed = random.random() / 2 #will be decided in genome
        self.direction = random.randint(1, 360)
        genderSeed = random.random()
        self.isMale = False
        if genderSeed > 0.5: # weighting will be decided in genome
            self.isMale = True # 50% chance of being male for now
            
        aggRand1 = random.randint(0, int(255 ** 0.5))
        aggRand2 = random.randint(0, int(255 ** 0.5))
        self.aggressionIndex = aggRand1 * aggRand2 # produces bell curve
        # aggression will be determined in genome (and hunger), with some random element
        # random for now
        

        

    def set(self):
        self.body.draw(self.environment)
        self.getColor()
            

    def wander(self):
        global speedMult
        speed = self.speed * speedMult
        try:
            #print(self.direction)
            angleRadians = self.direction * ((math.pi) / 180)
            xMovement = speed * math.cos(angleRadians)
            yMovement = speed * math.sin(angleRadians)
            self.body.move(xMovement, yMovement)
            position = self.body.getCenter()
            if position.getX() <= 5 or position.getX() >= 745:
                xMovement = -xMovement
                #print("X Movement: ", xMovement)
                #print("Y Movement: ", yMovement)
                #print("X Coord: ", position.getX())
                #print("Y Coord: ", position.getY())
                #print("-------------x-----------------")
                #print("-------------------------------")
                #print("-------------------------------")
                
            elif position.getY() <= 5 or position.getY() >= 745:
                yMovement = -yMovement

                #print("X Movement: ", xMovement)
                #print("Y Movement: ", yMovement)
                #print("X Coord: ", position.getX())
                #print("Y Coord: ", position.getY())
                #print("--------------y----------------")
                #print("-------------------------------")
                #print("-------------------------------")
                
            
            newDirection = math.atan2(yMovement, xMovement)
            self.direction = (180 * newDirection) / math.pi
        except(Exception):
            #do nothing
            print("err")
            
        
    def getColor(self):
        # color is defined by gender and aggression
        self.body.setOutline(color_rgb(self.aggressionIndex, 0, 0)) # more red when aggressive
        self.body.setFill("pink3")
        if self.isMale:
            self.body.setFill("blue")
        
            

class Chromosome:
    # chromosome class, every circle has one!
    # chromosome contains lots genes, which change over generations
    # genome is fixed length, made of one chromosome
    def __init__(self, genome):
        self.genome = genome # array of genes

    def mutate(self):
        # pick random gene
        genomeSize = len(self.genome)
        geneToChange = random.randint(0, genomeSize - 1)
        self.genome[geneToChange].mutate()

class Gene:
    # gene, consists of a name and genotype (AA/Aa/aA/aa),
    # and a phenotype it is tied to
    #genotype is expressed a boolean tuple
    
    def __init__(self, name, genotype, phenotype):
        self.name = name # eg. long legged
        self.genotype = genotype # eg. (False, True) - aA
        self.phenotype = phenotype # an array of everything this
        # gene effects, and how much it effects it, stored as tuples
        # eg. [("speed", 1.1), ("HP", 0.95), ...., ]

    def mutate(self):
        rand = random.random() # generate float between 1 and 0
        if rand > 0.99:
            # effect phenotype
            print()
        else:
            # effect genotype
            genoRand1 = random.randint(0,1)
            genoRand2 = random.randint(0,1)
            self.genotype = (bool(genoRand1), bool(genoRand2))
            
        
        
        

def getLine(point1, point2):
    line = Line(point1, point2)
    line.setFill("white")
    return line

def drawButton(environment, contents, xCoord, yCoord):
    # all buttons 30 by 30
    button = Rectangle(Point(xCoord - 15, yCoord - 15), Point(xCoord + 15, yCoord + 15))
    button.setOutline("white")
    text = Text(Point(xCoord, yCoord), contents)
    text.setFill("white")
    button.draw(environment)
    text.draw(environment)
    

def drawInterface(environment):
    statBarrier = getLine(Point(750, 0), Point(750, 751))
    statBarrier.draw(environment)

    controlBarrier = getLine(Point(750, 600), Point(1050, 600))
    controlBarrier.draw(environment)
    
    lblStats = Text(Point(900, 50), "STATS")
    lblStats.setFill("white")
    lblStats.draw(environment)

    drawButton(environment, "«", 825, 700)
    drawButton(environment, "◄◄", 875, 700)
    drawButton(environment, "| |", 925, 700)
    drawButton(environment, "»", 975, 700)

def updateButton(pausing, environment):
    blackout = Rectangle(Point(905, 680), Point(945, 720))
    blackout.setFill("black")
    blackout.draw(environment)
    if pausing:
        # change button to play
        drawButton(environment, "►", 925, 700)
    else:
        # change button to pause
        drawButton(environment, "| |", 925, 700)
        

def mouseAction(x, y, running, environment):
    global speedMult
    # mouse has been pressed
    if (x >= 810 and x <= 840 and y >= 685 and y <= 715):
        # slow down
        #print("slow down pressed")
        speedMult *= 0.5
        return True
    elif (x >= 860 and x <= 890 and y >= 685 and y <= 715):
        # rewind
        #print("rewind pressed")
        speedMult *= -1
        return True
    elif (x >= 910 and x <= 940 and y >= 685 and y <= 715):
        # pause/play
        updateButton(running, environment)
        if running:
            # change button to play
            return False
        # change button to pause
        return True
    elif (x >= 960 and x <= 990 and y >= 685 and y <= 715):
        # speed up
        #print("speed up pressed")
        speedMult *= 2
        return True
    else:
        print("search for organism")
        # search for organism, update stats
        return True
        
    
            
def createEnvironment():
    environment = GraphWin("Circles", 1050, 750)
    environment.setBackground("black")
    
    # RANDOMLY GENERATE FOOD (daves jawb)

    drawInterface(environment)

    return environment

def spawn(environment, n):
    organisms = []
    for i in range(n):
        organism = Organism(Point(i * 2,i * 2), environment)
        organisms.append(organism)
        organism.set()
    return organisms

def main():
    environment = createEnvironment()
    organisms = spawn(environment, 100)
    count = 0
    running = True
    while True: # organisms don't move when not running
        while running:
            # update stats
            organisms[count % 100].wander()
            count += 1
            # check for mouse clicks
            mouseClick = environment.checkMouse()
            if mouseClick != None: # else continue
                running = mouseAction(mouseClick.getX(), mouseClick.getY(), running, environment)
        mouseClick = environment.checkMouse()
        if mouseClick != None: # else continue
            running = mouseAction(mouseClick.getX(), mouseClick.getY(), running, environment)
        

    # render the environment, then wait for clicks

main()
