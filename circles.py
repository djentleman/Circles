## Todd And Daves 'Circles'

import time
import random
import math
from graphics import *
from threading import *

s = Semaphore() # implements mutal exclusion
speedMult = 1.0 # speed multiplier - global (for now)

class Organism:
    # circle class - the digital organism itself
    # phenotypes are attributes, eg: speed, vision...
    # ultimatley each organism will be running on a seperate thread
    def __init__(self, spawn, environment):
        self.spawn = spawn
        self.radius = (random.random() * 6) + 1  # radius is random for now
        self.mass = math.pi * (self.radius * self.radius)
        self.body = Circle(spawn, self.radius)
        self.alive = True # turns false when dead
        self.environment = environment
        self.speed = random.random() #will be decided in genome
        self.direction = random.randint(1, 360)
        genderSeed = random.random()
        self.isMale = False
        if genderSeed > 0.5: # weighting will be decided in genome
            self.isMale = True # 50% chance of being male for now
            
        aggRand1 = random.randint(1, int(255 ** 0.5))
        aggRand2 = random.randint(1, int(255 ** 0.5))
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
                #print("-------------y-----------------")
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

def getText(point, message):
    text = Text(point, message)
    text.setFill("white")
    return text

def drawButton(environment, contents, xCoord, yCoord):
    # all buttons 30 by 30
    button = Rectangle(Point(xCoord - 15, yCoord - 15), Point(xCoord + 15, yCoord + 15))
    button.setOutline("white")
    text = getText(Point(xCoord, yCoord), contents)
    button.draw(environment)
    text.draw(environment)
    

def drawInterface(environment):
    statBarrier = getLine(Point(750, 0), Point(750, 751))
    statBarrier.draw(environment)

    controlBarrier = getLine(Point(750, 650), Point(1050, 650))
    controlBarrier.draw(environment)
    
    lblStats = getText(Point(900, 30), "STATS")
    lblStats.setSize(18)
    lblStats.draw(environment)


    drawButton(environment, "«", 850, 700)
    drawButton(environment, "| |", 900, 700)
    drawButton(environment, "»", 950, 700)

def renderStats(environment):
    lblGenerals = getText(Point(900, 70), "General Stats")
    lblGenerals.draw(environment)
    
    titleBarrier = getLine(Point(765, 50), Point(1035, 50))
    titleBarrier.draw(environment)
    
    lblNoOfOrganisms = getText(Point(845, 100), "Number Of Organisms:")
    lblNoOfOrganisms.draw(environment)
    lblPlay = getText(Point(808, 130), "Play Speed:")
    lblPlay.draw(environment)
    
    generalBarrier = getLine(Point(765, 150), Point(1035, 150))
    generalBarrier.draw(environment)

    lblGenerals = getText(Point(900, 170), "Local Stats")
    lblGenerals.draw(environment)
    
    lblGender = getText(Point(794, 200), "Gender:")
    lblGender.draw(environment)
    lblAggression = getText(Point(808, 230), "Aggression:")
    lblAggression.draw(environment)
    lblDirection = getText(Point(799, 260), "Direction:")
    lblDirection.draw(environment)
    lblSpeed = getText(Point(791, 290), "Speed:")
    lblSpeed.draw(environment)
    lblMass = getText(Point(788, 320), "Mass:")
    lblMass.draw(environment)
    lblX = getText(Point(798, 350), "X-Coord:")
    lblX.draw(environment)
    lblY = getText(Point(798, 380), "Y-Coord:")
    lblY.draw(environment)

    stats = [] # array of stats

    noOfOrganisms = getText(Point(1000, 100), "-")
    noOfOrganisms.draw(environment)
    stats.append(noOfOrganisms) # index 0

    play = getText(Point(1000, 130), "-")
    play.draw(environment)
    stats.append(play) # index 1

    gender = getText(Point(1000, 200), "-")
    gender.draw(environment)
    stats.append(gender) # index 2

    aggression = getText(Point(1000, 230), "-")
    aggression.draw(environment)
    stats.append(aggression) # index 3

    direction = getText(Point(1000, 260), "-")
    direction.draw(environment)
    stats.append(direction) # index 4

    speed = getText(Point(1000, 290), "-")
    speed.draw(environment)
    stats.append(speed) # index 5

    mass = getText(Point(1000, 320), "-")
    mass.draw(environment)
    stats.append(mass) # index 6
    
    x = getText(Point(1000, 350), "-")
    x.draw(environment)
    stats.append(x) # index 7

    x = getText(Point(1000, 380), "-")
    x.draw(environment)
    stats.append(x) # index 8

    return stats
    


def updateButton(pausing, environment):
    blackout = Rectangle(Point(880, 680), Point(920, 720))
    blackout.setFill("black")
    blackout.draw(environment)
    if pausing:
        # change button to play
        drawButton(environment, "►", 900, 700)
    else:
        # change button to pause
        drawButton(environment, "| |", 900, 700)

def searchForOrganism(x, y, organisms, stats):
    resetColours(organisms) # reset colours
    organism = None
    for current in organisms:
        pos = current.body.getCenter()
        radius = current.body.getRadius()
        if x >= (pos.getX() - radius) and x <= (pos.getX() + radius) and \
           y >= (pos.getY() - radius) and y <= (pos.getY() + radius):
            organism = current
            break # break out of loop
    #update stats
    if organism == None:
        resetLocalStats(stats)
        return organism
    gender = "Female"
    if organism.isMale:
        gender = "Male"
    stats[2].setText(gender)
    stats[3].setText(organism.aggressionIndex)
    stats[4].setText(str("%.3f" % organism.direction) + "°")
    stats[5].setText("%.3f" % organism.speed)
    stats[6].setText("%.3f" % organism.mass)
    stats[7].setText("%.3f" % organism.body.getCenter().getX())
    stats[8].setText("%.3f" % organism.body.getCenter().getY())
    organism.body.setOutline("green")
    return organism
    
def resetColours(organisms):
    for organism in organisms:
         organism.body.setOutline(color_rgb(organism.aggressionIndex, 0, 0))
        
def resetLocalStats(stats):
    for index in range(2, len(stats)):
        stats[index].setText("-")
        

def mouseAction(x, y, running, environment, organisms, stats):
    global speedMult
    # mouse has been pressed
    if (x >= 835 and x <= 865 and y >= 685 and y <= 715):
        # slow down
        #print("slow down pressed")
        speedMult *= 0.5
        if speedMult < 0.03125:
            speedMult = 0.03125 # cap at 0.03125
        return running, None
    elif (x >= 885 and x <= 915 and y >= 685 and y <= 715):
        # pause/play
        updateButton(running, environment)
        if running:
            # change button to play
            return False, None
        # change button to pause
        return True, None
    elif (x >= 935 and x <= 965 and y >= 685 and y <= 715):
        # speed up
        #print("speed up pressed")
        speedMult *= 2
        if speedMult > 64:
            speedMult = 64.0 # cap at 64
        return running, None
    else:
        organism = searchForOrganism(x, y, organisms, stats)
        # search for organism, update stats
        return running, organism
        
    
            
def createEnvironment():
    environment = GraphWin("Circles", 1050, 750)
    environment.setBackground("black")
    
    # RANDOMLY GENERATE FOOD (daves jawb)

    drawInterface(environment)

    return environment

def spawn(environment, n):
    organisms = []
    for i in range(n):
        organism = Organism(Point(100, 100), environment)
        organisms.append(organism)
        organism.set()
    return organisms

def main():
    global speedMult
    environment = createEnvironment()
    stats = renderStats(environment) # changable stats are outputted as an array
    organisms = spawn(environment, 50)
    count = 0
    organism = None
    running = True
    while True: # organisms don't move when not running
        while running:
            #update stats
            stats[0].setText(len(organisms))
            stats[1].setText(str(speedMult) + "x")
            if organism != None and (count % 10 == 0):
                # this is a critical area - only important stats go here
                stats[4].setText(str("%.3f" % organism.direction) + "°")
                stats[5].setText("%.3f" % organism.speed)
                stats[7].setText("%.3f" % organism.body.getCenter().getX())
                stats[8].setText("%.3f" % organism.body.getCenter().getY())
            # -----------------
            organisms[count % 50].wander()
            count += 1
            # check for mouse clicks
            mouseClick = environment.checkMouse()
            if mouseClick != None: # else continue
                running, organism = mouseAction(mouseClick.getX(), mouseClick.getY(), running, environment, organisms, stats)
        stats[1].setText("Paused")
        mouseClick = environment.checkMouse()
        if mouseClick != None: # else continue
            running, organism = mouseAction(mouseClick.getX(), mouseClick.getY(), running, environment, organisms, stats)
        

    # render the environment, then wait for clicks

main()
