# circles prototype 2

import pygame, sys, time, random, math
from pygame.locals import *

from organism import *
from pygame_util import *
from interface import *
from food import *
from biomes import *
from genetics import *


def checkForOrganism(x, y, organisms):
    for organism in organisms:
        rad = organism.radius
        if x > organism.scrollX - rad and x < organism.scrollX + rad and \
           y > organism.scrollY - rad and y < organism.scrollY + rad:
            organism.focus()
            
            #print("organism focused")
            return organism
    return None

def purgeFocus(organisms, focus):
    for organism in organisms:
        if not organism == focus:
            organism.unFocus()
            

def runSim():    
    pygame.init()
    fpsClock = pygame.time.Clock()

    environment = pygame.display.set_mode((900, 650))
    pygame.display.set_caption('Circles v0.1.1')
    
    interface = Interface(environment)

    noOfOrganisms = 120
    noOfPlants = 0
    noOfCorpses = 0
    playSpeed = 1.0
    paused = False
    panelType = 0

    organisms = []
    for i in range(noOfOrganisms):
        randX = random.randint(0, 2000)
        randY = random.randint(0, 2000)
        organism = Organism(randX, randY, environment)
        organisms.append(organism)

    corpses = []

    plants = []
    biomes = []
    for i in range(10): # 5 biomes
        biome = Biome(1000, 1000)
        biome.x = random.randint(biome.radius, 2000 - biome.radius)
        biome.y = random.randint(biome.radius, 2000 - biome.radius)
        # this stops overflow
        plants = plants + biome.initBiome(environment)
        biomes.append(biome)
    noOfPlants = len(plants)
        
    simulationTime = 0.0
    frameRate = 0.0

    mousedown = False
    

    while True:
        start = time.clock()
        environment.fill(pygame.Color(0, 0, 0)) # erase
      
        for event in pygame.event.get(): # this makes it stable!
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #elif event.type == MOUSEMOTION:
            #    mousex, mousey = event.pos
            #    # hover goes here
            #    print(mousex, mousey)
            elif event.type == MOUSEBUTTONDOWN:
                mousedown = True
                mousex, mousey = event.pos
                pressed = interface.handleButtonPress(mousex, mousey)
                if not pressed:
                    interface.focus = checkForOrganism(mousex, mousey, organisms)
                    interface.graphArray = []
                    purgeFocus(organisms, interface.focus)
                    # purges focus on non focused organisms
                else:
                    playSpeed = interface.playSpeed
                    paused = interface.paused
            elif event.type == MOUSEBUTTONUP:
                mousedown = False
        
                
        if mousedown:
            relx, rely = pygame.mouse.get_rel()
            interface.scrollX -= relx
            interface.scrollY -= rely
            if interface.scrollX > 420:
                interface.scrollX = 420
            elif interface.scrollX < 0:
                interface.scrollX = 0
            if interface.scrollY > 420:
                interface.scrollY = 420
            elif interface.scrollY < 0:
                interface.scrollY = 0
        pygame.mouse.get_rel() # reset
        
        if not paused:
            plants = []
            for biome in biomes:
                plants = plants + biome.grow(playSpeed, environment)

        for plant in plants:
            #3.33 = 2000 / 600
            plant.draw(interface.scrollX * 3.33, interface.scrollY * 3.33)
        
        for corpse in corpses:
            if not paused:
                alive = not corpse.rot(playSpeed)
                if not alive:
                    corpses.remove(corpse)
            corpse.draw(interface.scrollX * 3.33, interface.scrollY * 3.33)

        for organism in organisms:
            organism.draw(interface.scrollX * 3.33, interface.scrollY * 3.33) # need to be drawn in order to interact

        for organism in organisms:
            # organism does it's stuff
            if not paused:
                alive, potentialFood = organism.move(playSpeed, [organisms, corpses, plants])
                organisms = potentialFood[0]
                corpses = potentialFood[1]
                plants = potentialFood[2]
                if not alive:
                    # organism has died
                    corpse = organism.getCorpse()
                    organisms.remove(organism)
                    corpses.append(corpse)
            
        interface.draw() # everything rendered here is invisible to the organisms

        noOfOrganisms = len(organisms)
        noOfPlants = len(plants)
        noOfCorpses = len(corpses)

        interface.updateGlobalStats(noOfOrganisms, noOfPlants + noOfCorpses, playSpeed,
                          frameRate, simulationTime)

        pygame.display.update() # update display

        
        end = time.clock()
        if not paused:
            simulationTime += ((end - start) * playSpeed)
        frameRate = float(1 / (end - start))

def main():
    runSim()

main()
