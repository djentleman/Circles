#pygame test

import pygame, sys, time, random, math
from pygame.locals import *

from organism import *
from pygame_util import *
from interface import *
from food import *

def checkForOrganism(x, y, organisms):
    for organism in organisms:
        rad = organism.radius
        if x > organism.x - rad and x < organism.x + rad and \
           y > organism.y - rad and y < organism.y + rad:
            organism.focus()
            
            #print("organism focused")
            return organism
    return None

def purgeFocus(organisms, focus):
    for organism in organisms:
        if not organism == focus:
            organism.unFocus()

def runSim():    
    pygame.init() # lol pygame is so gay
    fpsClock = pygame.time.Clock()

    environment = pygame.display.set_mode((900, 650))
    pygame.display.set_caption('Circles v1.1')
    
    interface = Interface(environment)

    noOfOrganisms = 30
    noOfPlants = 50
    noOfCorpses = 0
    playSpeed = 1.0
    paused = False
    panelType = 0

    organisms = []
    for i in range(noOfOrganisms):
        randX = random.randint(0, 650)
        randY = random.randint(0, 650)
        organism = Organism(randX, randY, environment)
        organisms.append(organism)

    corpses = []

    plants = []
    for i in range(noOfPlants):
        isPoison = random.random()
        randX = random.randint(0, 650)
        randY = random.randint(0, 650)
        if isPoison < 0.92:
            plant = Plant(randX, randY, environment)
        else:
            plant = PoisonPlant(randX, randY, environment)
        plants.append(plant)
        
    simulationTime = 0.0
    frameRate = ""

    while True:
        start = time.clock()
        environment.fill(pygame.Color(0, 0, 0)) # erase

        purgeFocus(organisms, interface.focus) # purges focus on non focused organisms
      
        for event in pygame.event.get(): # this makes it stable!
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                # hover goes here
                #print(mousex, mousey)
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                pressed = interface.handleButtonPress(mousex, mousey)
                if not pressed:
                    interface.focus = checkForOrganism(mousex, mousey, organisms)
                else:
                    playSpeed = interface.playSpeed
                    paused = interface.paused

        for plant in plants:
            #plant does it's stuff
            if not paused:
                plant.grow(playSpeed)
                if plant.eaten:
                    plants.remove(plant)
                
            plant.draw()

        for corpse in corpses:
            if not paused:
                alive = not corpse.rot(playSpeed)
                if not alive:
                    corpses.remove(corpse)
            corpse.draw()

        for organism in organisms:
            organism.draw() # need to be drawn in order to interact

        for organism in organisms:
            # organism does it's stuff
            if not paused:
                alive = organism.move(playSpeed)
                if not alive:
                    # organism has died
                    corpse = organism.getCorpse()
                    organisms.remove(organism)
                    corpses.append(corpse)
            
        interface.updateLocalStats()
        interface.outLineSidePanel()
        
        interface.initGlobalStats()
        interface.renderGlobalStats()
        interface.initSidePanel()
        interface.renderSidePanel()
        interface.drawButtons()

        noOfOrganisms = len(organisms)
        noOfPlants = len(plants)
        noOfCorpses = len(corpses)

        interface.updateGlobalStats(noOfOrganisms, noOfPlants + noOfCorpses, playSpeed,
                          frameRate, simulationTime)

        pygame.display.update() # update display

        
        end = time.clock()
        if not paused:
            simulationTime += ((end - start) * playSpeed)
        frameRate = ("%.2f" % float(1 / (end - start)))

def main():
    runSim()

main()
