#pygame test

import pygame, sys, time, random, math
from pygame.locals import *

from organism import *
from pygame_util import *
    

def initStats(environment):
    drawText(environment, "Global Stats", 720, 10, 18)
    drawText(environment, "Number Of Organisms:", 660, 40, 12)
    drawText(environment, "Play Speed:", 660, 60, 12)
    drawText(environment, "Frame Rate:", 660, 80, 12)
    drawText(environment, "Local Stats", 720, 160, 18)
    drawText(environment, "Gender:", 660, 190, 12)
    drawText(environment, "Aggression:", 660, 210, 12)
    drawText(environment, "Direction:", 660, 230, 12)
    drawText(environment, "Speed:", 660, 250, 12)
    drawText(environment, "Mass:", 660, 270, 12)
    drawText(environment, "X-Coord:", 660, 290, 12)
    drawText(environment, "Y-Coord:", 660, 310, 12)
    drawText(environment, "Energy:", 660, 330, 12)

def renderStats(environment, stats):
    # stats is an array of stats
    drawText(environment, str(stats[0]), 850, 40, 12)
    drawText(environment, str(stats[1]), 850, 60, 12)
    drawText(environment, str(stats[2]), 850, 80, 12)
    drawText(environment, str(stats[3]), 850, 190, 12)
    drawText(environment, str(stats[4]), 850, 210, 12)
    drawText(environment, str(stats[5]), 850, 230, 12)
    drawText(environment, str(stats[6]), 850, 250, 12)
    drawText(environment, str(stats[7]), 850, 270, 12)
    drawText(environment, str(stats[8]), 850, 290, 12)
    drawText(environment, str(stats[9]), 850, 310, 12)
    drawText(environment, str(stats[10]), 850, 330, 12)
    
    

def purgeFocus(organisms, focus):
    for organism in organisms:
        if not organism == focus:
            organism.unFocus()
    
def checkForOrganism(x, y, organisms):
    for organism in organisms:
        rad = organism.radius
        if x > organism.x - rad and x < organism.x + rad and \
           y > organism.y - rad and y < organism.y + rad:
            organism.focus()
            #print("organism focused")
            return organism
    return None

def updateLocalStats(focus, stats):
    if focus == None:
        for i in range(3, len(stats) - 1):
            stats[i] = "-"
    else:
        if focus.isMale:
            stats[3] = "Male"
        else:
            stats[3] = "Female"
        stats[4] = "%.2f" % focus.aggression
        stats[5] = "%.2f" % focus.direction
        stats[6] = "%.2f" % focus.speed
        stats[7] = "%.2f" % focus.mass
        stats[8] = "%.2f" % focus.actualX
        stats[9] = "%.2f" % focus.actualY
        stats[10] = "%.2f" % focus.energy
    #print(stats)

    return stats

def runSim():    
    pygame.init() # lol pygame is so gay
    fpsClock = pygame.time.Clock()

    environment = pygame.display.set_mode((900, 650))
    pygame.display.set_caption('Circles v1.1')

    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    msg = "hello world"

    stats = [0, 0, "-", "-", "-", "-", "-", "-", "-", "-", "-"]

    noOfOrganisms = 115
    stats[0] = (noOfOrganisms)
    playSpeed = 1.0
    stats[1] = (playSpeed)


    organisms = []
    for i in range(noOfOrganisms):
        randX = random.randint(0, 650)
        randY = random.randint(0, 650)
        organism = Organism(randX, randY, environment)
        organisms.append(organism)


    white = pygame.Color(255, 255, 255)
    i = 0

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
      

        initStats(environment)


        
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
                focus = checkForOrganism(mousex, mousey, organisms)
                #print(mousex, mousey)
        stats = updateLocalStats(focus, stats)
                    
                
            # check if any thing is hovering
            #print(event)
        #print(i)

        for organism in organisms:
            # organism does it's stuff
            organism.move()
            organism.draw()

        #update stats
        renderStats(environment, stats)


            
        
        # tell stuff to move
        pygame.display.update() # update display
        fpsClock.tick() # runs at 60 frames, this decides how fluid the program is

        end = time.clock()
        stats[2] = ("%.2f" % float(1 / (end - start)))


def main():
    runSim()

main()
