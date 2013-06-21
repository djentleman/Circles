#pygame test

import pygame, sys, time, random, math
from pygame.locals import *

from organism import *
from pygame_util import *
from interface import *
from food import *


def runSim():    
    pygame.init() # lol pygame is so gay
    fpsClock = pygame.time.Clock()

    environment = pygame.display.set_mode((900, 650))
    pygame.display.set_caption('Circles v1.1')
    
    stats = [0, 0, 0, 0, "-", "-", "-", "-", "-", "-", "-", "-", "-"]
    vision = None
    #all the stats will be contained in the OO interface

    noOfOrganisms = 30
    noOfPlants = 50
    noOfCorpses = 0
    stats[0] = noOfOrganisms
    stats[1] = noOfPlants
    playSpeed = 1.0
    paused = False
    stats[2] = (playSpeed)
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
        


    white = rgb(255, 255, 255)

    focus = None
    simulationTime = 0

    while True:
        start = time.clock()
        environment.fill(pygame.Color(0, 0, 0)) # erase




        
        purgeFocus(organisms, focus) # purges focus on non focused organisms


        
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
                
                oldPlaySpeed = playSpeed
                playSpeed = handlePlaySpeedChange(mousex, mousey, playSpeed)
                stats[2] = playSpeed
                if not (playSpeed == oldPlaySpeed):
                    if playSpeed > 32.0 or playSpeed < 0.02:
                        playSpeed = oldPlaySpeed
                    # apply any neccecary caps
                    break # playspeed changed
                
                oldPaused = paused
                paused = handlePauseButton(mousex, mousey, paused)
                if paused:
                    stats[2] = "Paused"
                else:
                    stats[2] = playSpeed
                if not (paused == oldPaused):
                    # state has changed
                    break # pause button pressed
                
                oldPanelType = panelType
                panelType = handlePanelTypeChange(mousex, mousey, panelType)
                newPanelType = panelType
                if not (newPanelType == oldPanelType):
                    # one of these buttons was pressed
                    break
                
                focus = checkForOrganism(mousex, mousey, organisms)
                #print(mousex, mousey)
                
        if focus == None:
            vision = None
        else:
            vision = focus.vision # what the focused one can see
        

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
            

        # draw interface on top of everything


        #block
        pygame.draw.rect(environment, rgb(0, 0, 0), (650, 0, 300, 650), 0)

        drawButtons(environment, paused) # buttons mightbe hovering        
        #update stats
        stats = updateLocalStats(focus, stats)
        renderStats(environment, stats) # globals
        renderSidePanel(environment, panelType, stats, vision)
                # render a line
        pygame.draw.line(environment, white, 
                         (650, 0), (650, 650), 2)
        pygame.draw.line(environment, white, 
                         (650, 150), (900, 150), 2)
        pygame.draw.line(environment, white, 
                         (650, 550), (900, 550), 2)
      

        initStats(environment) # inits globals
        initSidePanel(environment, panelType)

        
        
        # tell stuff to move
        pygame.display.update() # update display
        fpsClock.tick(60) # runs at 60 frames max, this decides how fluid the program is



        noOfOrganisms = len(organisms)
        noOfPlants = len(plants)
        noOfCorpses = len(corpses)
        stats[0] = noOfOrganisms
        stats[1] = noOfPlants + noOfCorpses

        end = time.clock()
        stats[3] = ("%.2f" % float(1 / (end - start)))
        if not paused:
            simulationTime += ((end - start) * playSpeed)
        stats[4] = ("%.2f" % simulationTime + "s")



def main():
    runSim()

main()
