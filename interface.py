          


# library imports
import time
import random
import math
from graphics import *
from threading import *        

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

    # draw sight reticule - within the box, you will be able to see what the
    # focused circle sees
    sight = Rectangle(Point(770, 600), Point(1030, 605))
    sight.setOutline("white")
    sight.draw(environment)

    upperReticule = getLine(Point(900, 600), Point(900, 580))
    upperReticule.draw(environment)
    lowerReticule = getLine(Point(900, 605), Point(900, 625))
    lowerReticule.draw(environment)

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
    lblEnergy = getText(Point(793, 410), "Energy:")
    lblEnergy.draw(environment)

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

    energy = getText(Point(1000, 410), "-")
    energy.draw(environment)
    stats.append(energy) # index 9

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

            
def createEnvironment():
    environment = GraphWin("Circles", 1050, 750)
    environment.setBackground("black")

    drawInterface(environment)

    return environment

def spawn(environment, n):
    organisms = []
    for i in range(n):
        organism = Organism(Point(100, 100), environment)
        organisms.append(organism)
        organism.set()
    return organisms


def generateFood(environment):
    # generates food in random areas
    # food is all rgb(0, 255, 255) for now
    allFood = []
    clusters = []

    numberOfClusters = random.randint(6,10)
    for i in range(numberOfClusters):
        randX = random.randint(0, 750)
        randY = random.randint(0, 750)
        cluster = FoodCluster(randX, randY, environment)
        food = cluster.generateCluster()
        allFood = food + allFood
        clusters.append(cluster)
        
    return allFood, clusters
