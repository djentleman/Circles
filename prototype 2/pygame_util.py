# pygame util
import pygame, sys, time, random, math

def rgb(r, g, b):
    return pygame.Color(r, g, b) # makes life easier!


def drawText(environment, msg, x, y, size):
    fontObj = pygame.font.Font('freesansbold.ttf', size)
    msgSurfaceObj = fontObj.render(msg, False, rgb(255, 255, 255))
    environment.blit(msgSurfaceObj, (x, y))

def drawButton(environment, msg, x, y, width, height):
    # add possible hover/focus animation
    pygame.draw.rect(environment, rgb(255, 255, 255),
                     (x - 20, y - 20, width, height), 1)
    drawText(environment, msg, x - int(width / 5), y - int(height / 4), 18)
    # text positioning needs work

    
    
