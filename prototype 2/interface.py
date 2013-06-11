# interface

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
        for i in range(3, len(stats)):
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

def drawButtons(environment, paused):
    drawButton(environment, "«", 725, 600)
    if paused:
        drawButton(environment, ">", 775, 600)
    else:
        drawButton(environment, "| |", 775, 600)
    drawButton(environment, "»", 825, 600)



def handlePlaySpeedChange(x, y, playSpeed):
    if x > 705 and x < 745 and \
       y > 580 and y < 620:
        playSpeed *= 0.5 # slow speed
    elif x > 805 and x < 845 and \
         y > 580 and y < 620:
        playSpeed *= 2 # increase speed
    return playSpeed

def handlePauseButton(x, y, paused):
    if x > 755 and x < 795 and \
       y > 580 and y < 620:
        # button pressed
        paused = not paused # flip
    return paused
