# interface

import pygame, sys, time, random, math
from pygame.locals import *

from organism import *
from pygame_util import *

# next version - an OO interface
# stats and focused would be attributes
# which reduces variables being passed around

def initStats(environment):
    drawText(environment, "Global Stats", 720, 10, 18)
    drawText(environment, "Number Of Organisms:", 660, 40, 12)
    drawText(environment, "Number Of Food Items:", 660, 60, 12)
    drawText(environment, "Play Speed:", 660, 80, 12)
    drawText(environment, "Frame Rate:", 660, 100, 12)

def renderStats(environment, stats):
    # stats is an array of stats
    drawText(environment, str(stats[0]), 850, 40, 12)
    drawText(environment, str(stats[1]), 850, 60, 12)
    drawText(environment, str(stats[2]), 850, 80, 12)
    drawText(environment, str(stats[3]), 850, 100, 12)

def initLocalStats(environment):
    drawText(environment, "Local Stats", 720, 160, 18)
    drawText(environment, "Gender:", 660, 190, 12)
    drawText(environment, "Aggression:", 660, 210, 12)
    drawText(environment, "Direction:", 660, 230, 12)
    drawText(environment, "Speed:", 660, 250, 12)
    drawText(environment, "Mass:", 660, 270, 12)
    drawText(environment, "X-Coord:", 660, 290, 12)
    drawText(environment, "Y-Coord:", 660, 310, 12)
    drawText(environment, "Energy:", 660, 330, 12)

def renderLocalStats(environment, stats):
    drawText(environment, str(stats[4]), 850, 190, 12)
    drawText(environment, str(stats[5]), 850, 210, 12)
    drawText(environment, str(stats[6]), 850, 230, 12)
    drawText(environment, str(stats[7]), 850, 250, 12)
    drawText(environment, str(stats[8]), 850, 270, 12)
    drawText(environment, str(stats[9]), 850, 290, 12)
    drawText(environment, str(stats[10]), 850, 310, 12)
    drawText(environment, str(stats[11]), 850, 330, 12)

def initInputs(environment):
    drawText(environment, "Inputs", 745, 160, 18)
    # sight reticule from v1.0
    drawText(environment, "Sight:", 660, 220, 12)
    pygame.draw.rect(environment, rgb(255, 255, 255),
                     (675, 250, 200, 5), 1)
    pygame.draw.line(environment, rgb(255, 255, 255),
                     (775, 250), (775, 235), 2)
    pygame.draw.line(environment, rgb(255, 255, 255),
                     (775, 255), (775, 270), 2)

def initGenetics(environment):
    drawText(environment, "Genetics", 720, 160, 18)

    drawGraphSelect(environment, "Highlight Species", 750, 470, 140, False)

def initGraphs(environment):
    drawText(environment, "Graphs", 740, 160, 18)
    pygame.draw.line(environment, rgb(255, 255, 255),
                     (700, 200), (700, 360), 2)
    pygame.draw.line(environment, rgb(255, 255, 255),
                     (690, 350), (850, 350), 2)
    # graph is rendered using a pixelarray

    # buttons
    drawGraphSelect(environment, "Speed", 710, 400, 90, True)
    drawGraphSelect(environment, "Aggression", 710, 430, 90, False)
    drawGraphSelect(environment, "Energy", 710, 460, 90, False)
    drawGraphSelect(environment, "Direction", 840, 400, 90, False)
    drawGraphSelect(environment, "Mass", 840, 430, 90, False)
    drawGraphSelect(environment, "Radius", 840, 460, 90, False)
    
    
    
    

def initNothing(environment):
    drawText(environment, "None", 720, 160, 18)
    
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
        for i in range(4, len(stats)):
            stats[i] = "-"
    else:
        if focus.isMale:
            stats[4] = "Male"
        else:
            stats[4] = "Female"
        stats[5] = "%.2f" % focus.aggression
        stats[6] = "%.2f" % focus.direction
        stats[7] = "%.2f" % focus.speed
        stats[8] = "%.2f" % focus.mass
        stats[9] = "%.2f" % focus.actualX
        stats[10] = "%.2f" % focus.actualY
        stats[11] = "%.2f" % focus.energy
    #print(stats)

    return stats

def drawButtons(environment, paused):
    drawButton(environment, "«", 725, 600, 40, 40)
    if paused:
        drawButton(environment, ">", 775, 600, 40, 40)
    else:
        drawButton(environment, "| |", 775, 600, 40, 40)
    drawButton(environment, "»", 825, 600, 40, 40)
    # control buttons drawn


def initSidePanel(environment, panelType):
    # sidePanelType is an integer
    # 0 = local stats
    # 1 = input visulization
    # 2 = genetics
    # 3 = RT graphs
    if panelType == 0:
        initLocalStats(environment)
    elif panelType == 1:
        initInputs(environment)
    elif panelType == 2:
        initGenetics(environment)
    elif panelType == 3:
        initGraphs(environment)
    else: # panelType == 4:
        initNothing(environment)
    
    # now draw display change arrows
    drawButton(environment, "<-", 680, 520, 40, 40)
    drawButton(environment, "->", 870, 520, 40, 40)


def renderSidePanel(environment, panelType, stats):
    if panelType == 0:
        renderLocalStats(environment, stats)
    



    
def handlePanelTypeChange(x, y, panelType):
    if x > 660 and x < 700 and \
       y > 500 and y < 540:
        panelType -= 1
    elif x > 850 and x < 890 and \
         y > 500 and y < 540:
        panelType += 1
    if panelType > 4:
        panelType = 0
    if panelType < 0:
        panelType = 4
    return panelType

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
