# interface

import pygame, sys, time, random, math
from pygame.locals import *

from organism import *
from pygame_util import *

class Interface:
    def __init__(self, environment):
        self.focus = None
        self.panelType = 0 # defaults on stats page
        self.environment = environment
        
        self.globalStats = ["-", "-", "-", "-", "-"]
        self.localStats = ["-", "-", "-", "-", "-", "-", "-", "-"]

        self.graphArray = [] # updates as graph updates
        self.graphType = 0 # number between 0 and 5

        self.paused = False
        self.playSpeed = 1.0

    def outLineSidePanel(self):
        pygame.draw.rect(self.environment, rgb(0, 0, 0), (650, 0, 300, 650), 0)
        pygame.draw.line(self.environment, rgb(255, 255, 255), 
                         (650, 0), (650, 650), 2)
        pygame.draw.line(self.environment, rgb(255, 255, 255), 
                         (650, 150), (900, 150), 2)
        pygame.draw.line(self.environment, rgb(255, 255, 255), 
                         (650, 550), (900, 550), 2)

    def drawButtons(self):
        drawButton(self.environment, "«", 725, 600, 40, 40)
        if self.paused:
            drawButton(self.environment, ">", 775, 600, 40, 40)
        else:
            drawButton(self.environment, "| |", 775, 600, 40, 40)
        drawButton(self.environment, "»", 825, 600, 40, 40)
        # control buttons drawn

    def initSidePanel(self):
        # sidePanelType is an integer
        # 0 = local stats
        # 1 = input visulization
        # 2 = genetics
        # 3 = RT graphs
        if self.panelType == 0:
            self.initLocalStats()
        elif self.panelType == 1:
            self.initInputs()
        elif self.panelType == 2:
            self.initGenetics()
        elif self.panelType == 3:
            self.initGraphs()
        else: # panelType == 4:
            self.initNothing()

    def renderSidePanel(self):
        if self.panelType == 0:
            self.renderLocalStats()
        elif self.panelType == 1:
            self.renderInputs()
        elif self.panelType == 3:
            self.renderGraphs() 
    
    # now draw display change arrows
        drawButton(self.environment, "<-", 680, 520, 40, 40)
        drawButton(self.environment, "->", 870, 520, 40, 40)

    def updateGlobalStats(self, noOfOrganisms, noOfFood,
                          playSpeed, frameRate, simTime):
        self.globalStats[0] = noOfOrganisms
        self.globalStats[1] = noOfFood
        self.globalStats[2] = playSpeed
        self.globalStats[3] = frameRate
        self.globalStats[4] = simTime

    def updateLocalStats(self):
        if self.focus == None:
            for i in range(len(self.localStats)):
                self.localStats[i] = "-"
        else:
            if self.focus.isMale:
                self.localStats[0] = "Male"
            else:
                self.localStats[0] = "Female"
            self.localStats[1] = "%.2f" % self.focus.aggression
            self.localStats[2] = "%.2f" % self.focus.direction
            self.localStats[3] = "%.2f" % self.focus.speed
            self.localStats[4] = "%.2f" % self.focus.mass
            self.localStats[5] = "%.2f" % self.focus.actualX
            self.localStats[6] = "%.2f" % self.focus.actualY
            self.localStats[7] = "%.2f" % self.focus.energy

    def initGlobalStats(self):
        drawText(self.environment, "Global Stats", 720, 10, 18)
        drawText(self.environment, "Number Of Organisms:", 660, 40, 12)
        drawText(self.environment, "Number Of Food Items:", 660, 60, 12)
        drawText(self.environment, "Play Speed:", 660, 80, 12)
        drawText(self.environment, "Frame Rate:", 660, 100, 12)
        drawText(self.environment, "Simulation Time:", 660, 120, 12)

    def renderGlobalStats(self):
        drawText(self.environment, str(self.globalStats[0]), 850, 40, 12)
        drawText(self.environment, str(self.globalStats[1]), 850, 60, 12)
        drawText(self.environment, str(self.globalStats[2]), 850, 80, 12)
        drawText(self.environment, str(self.globalStats[3]), 850, 100, 12)
        drawText(self.environment, str(self.globalStats[4]), 850, 120, 12)
        
    def initLocalStats(self):
        drawText(self.environment, "Local Stats", 720, 160, 18)
        drawText(self.environment, "Gender:", 660, 190, 12)
        drawText(self.environment, "Aggression:", 660, 210, 12)
        drawText(self.environment, "Direction:", 660, 230, 12)
        drawText(self.environment, "Speed:", 660, 250, 12)
        drawText(self.environment, "Mass:", 660, 270, 12)
        drawText(self.environment, "X-Coord:", 660, 290, 12)
        drawText(self.environment, "Y-Coord:", 660, 310, 12)
        drawText(self.environment, "Energy:", 660, 330, 12)

    def renderLocalStats(self):
        drawText(self.environment, str(self.localStats[0]), 850, 190, 12)
        drawText(self.environment, str(self.localStats[1]), 850, 210, 12)
        drawText(self.environment, str(self.localStats[2]), 850, 230, 12)
        drawText(self.environment, str(self.localStats[3]), 850, 250, 12)
        drawText(self.environment, str(self.localStats[4]), 850, 270, 12)
        drawText(self.environment, str(self.localStats[5]), 850, 290, 12)
        drawText(self.environment, str(self.localStats[6]), 850, 310, 12)
        drawText(self.environment, str(self.localStats[7]), 850, 330, 12)

    def initInputs(self):
        drawText(self.environment, "Inputs", 745, 160, 18)
        # sight reticule from v1.0
        drawText(self.environment, "Sight:", 660, 220, 12)
        pygame.draw.rect(self.environment, rgb(255, 255, 255),
                         (675, 250, 200, 8), 1)
        pygame.draw.line(self.environment, rgb(255, 255, 255),
                         (775, 250), (775, 235), 2)
        pygame.draw.line(self.environment, rgb(255, 255, 255),
                         (775, 258), (775, 273), 2)

    def renderInputs(self):
        if self.focus != None:
            vision = self.focus.vision
            # we have vision
            # each block is 5 x 5 pixels
        
            width = 198 / len(vision)
        
            currentX = 676
            for current in vision:
                pygame.draw.rect(self.environment, current,
                             (currentX, 251, width, 6), 0)
                currentX += width # we have the reverse image
               
    def initGenetics(self):
        drawText(self.environment, "Genetics", 720, 160, 18)
        drawGraphSelect(self.environment, "Highlight Species", 750, 470, 140, False)

    def initGraphs(self):
        drawText(self.environment, "Graphs", 740, 160, 18)
        pygame.draw.line(self.environment, rgb(255, 255, 255),
                         (700, 200), (700, 360), 2)
        pygame.draw.line(self.environment, rgb(255, 255, 255),
                         (690, 350), (850, 350), 2)
        
        pygame.draw.line(self.environment, rgb(255, 255, 255),
                         (695, 200), (705, 200), 1)
        pygame.draw.line(self.environment, rgb(255, 255, 255),
                         (695, 275), (705, 275), 1)
        pygame.draw.line(self.environment, rgb(255, 255, 255),
                         (850, 345), (850, 355), 1)
        pygame.draw.line(self.environment, rgb(255, 255, 255),
                         (775, 345), (775, 355), 1)
        
        for currentY in range(215, 350, 15):
            pygame.draw.line(self.environment, rgb(255, 255, 255),
                             (698, currentY), (702, currentY), 1)
        for currentX in range(835, 700, -15):
            pygame.draw.line(self.environment, rgb(255, 255, 255),
                             (currentX, 348), (currentX, 352), 1)
            
        # graph is rendered using a pixelarray

        # buttons
        statNames = ["Speed", "Aggression", "Energy",
                     "Direction", "Mass", "Radius"]
        currentX = 710
        currentY = 400
        for index in range(len(statNames)):
            if index == self.graphType:
                drawGraphSelect(self.environment, statNames[index],
                                currentX, currentY, 90, True)
            else:
                drawGraphSelect(self.environment, statNames[index],
                                currentX, currentY, 90, False)
            currentY += 30
            if currentY > 460:
                currentX += 130
                currentY = 400

    def renderGraphs(self):
        if self.focus != None:
            for i in range(len(self.graphArray) - 1):
                self.graphArray[i] = (self.graphArray[i][0] - 1,
                                      self.graphArray[i][1])
                if self.graphArray[i][0] < 700:
                    self.graphArray.remove(self.graphArray[i])
                    break
            # multipliers are calculated by 1 /(n(max) / h) = 1 / (n(max) / 150)
            # max radius = 15
            maxY = ""
            midY = ""
            if self.graphType == 0:
                self.graphArray.append((850, 350 - int(self.focus.speed * 100)))
                maxY = "1.5"
                midY = "0.75"
            elif self.graphType == 1:
                self.graphArray.append((850, 350 - int(self.focus.aggression / 1.7)))
                maxY = "255"
                midY = "127.5"
            elif self.graphType == 2:
                self.graphArray.append((850, 350 - int(self.focus.energy)))
                maxY = "150"
                midY = "75"
            elif self.graphType == 3:
                self.graphArray.append((850, 350 - int(self.focus.direction / 2.4)))
                maxY = "360"
                midY = "180"
            elif self.graphType == 4:
                self.graphArray.append((850, 350 - int(self.focus.mass / 4.71)))
                maxY = "700"
                midY = "350"
            elif self.graphType == 5:
                self.graphArray.append((850, 350 - int(self.focus.actualRadius * 10)))
                maxY = "15"
                midY = "7.5"

            maxX = ("%.2f" % self.globalStats[4] + "s")
                
            drawText(self.environment, maxY, 670, 197, 10)
            drawText(self.environment, midY, 670, 272, 10)
            drawText(self.environment, maxX, 840, 360, 10)

            for pixel in self.graphArray:
                self.environment.set_at(pixel, rgb(0, 255, 0))
        else:
            self.graphArray = []

    def initNothing(self):                                
        drawText(self.environment, "None", 750, 160, 18)

    def handleButtonPress(self, x, y):
        #returns true if a button is potentially pressed
        if x < 650:
            return False
        self.panelType = handlePanelTypeChange(x, y, self.panelType)
        self.playSpeed = handlePlaySpeedChange(x, y, self.playSpeed)
        self.paused = handlePauseButtonChange(x, y, self.paused)
        newGraphType = handleGraphButtonChange(x, y)
        if newGraphType != None and self.panelType == 3:
            self.graphType = newGraphType
            self.graphArray = []
        return True
             
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

def handlePauseButtonChange(x, y, paused):
    if x > 755 and x < 795 and \
       y > 580 and y < 620:
        # button pressed
        paused = not paused # flip
    return paused

def handleGraphButtonChange(x, y):
    if x > 665 and x < 755 and \
       y > 390 and y < 410:
        return 0
    if x > 665 and x < 755 and \
       y > 420 and y < 440:
        return 1
    if x > 665 and x < 755 and \
       y > 450 and y < 470:
        return 2
    if x > 795 and x < 885 and \
       y > 390 and y < 410:
        return 3
    if x > 795 and x < 885 and \
       y > 420 and y < 440:
        return 4
    if x > 795 and x < 885 and \
       y > 450 and y < 470:
        return 5
    else:
        return None
    
        

