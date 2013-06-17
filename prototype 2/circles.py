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
    
    stats = [0, 0, 0, "-", "-", "-", "-", "-", "-", "-", "-", "-"]
    #all the stats will be contained in the OO interface

    noOfOrganisms = 15
    noOfPlants = 50
    stats[0] = (noOfOrganisms)
    stats[1] = (noOfPlants)
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

    plants = []
    for i in range(noOfPlants):
        randX = random.randint(0, 650)
        randY = random.randint(0, 650)
        plant = Plant(randX, randY, environment)
        plants.append(plant)
        


    white = rgb(255, 255, 255)

    focus = None

    while True:
        start = time.clock()
        environment.fill(pygame.Color(0, 0, 0)) # erase

        # render a line
        pygame.draw.line(environment, white, 
                         (650, 0), (650, 650), 2)
        pygame.draw.line(environment, white, 
                         (650, 150), (900, 150), 2)
        pygame.draw.line(environment, white, 
                         (650, 550), (900, 550), 2)
      

        initStats(environment) # inits globals
        initSidePanel(environment, panelType)


        
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
                newPlaySpeed = playSpeed
                if not (newPlaySpeed == oldPlaySpeed):
                    # apply any neccecary caps
                    break # playspeed changed
                
                oldPaused = paused
                paused = handlePauseButton(mousex, mousey, paused)
                if paused:
                    stats[2] = "Paused"
                else:
                    stats[2] = playSpeed
                newPaused = paused
                if not (newPaused == oldPaused):
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
                


        
        drawButtons(environment, paused) # buttons mightbe hovering
                    
        for organism in organisms:
            # organism does it's stuff
            if not paused:
                organism.move(playSpeed)#
                organism.traceRay(0)
            organism.draw()

        for plant in plants:
            #plant does it's stuff
            if not paused:
                plant.grow()
            plant.draw()

        #update stats
        stats = updateLocalStats(focus, stats)
        renderStats(environment, stats) # globals
        renderSidePanel(environment, panelType, stats)


            
        
        # tell stuff to move
        pygame.display.update() # update display
        fpsClock.tick(60) # runs at 60 frames, this decides how fluid the program is

        end = time.clock()
        stats[3] = ("%.2f" % float(1 / (end - start)))


def main():
    runSim()

main()
