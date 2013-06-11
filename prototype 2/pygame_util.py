# pygame util
import pygame, sys, time, random, math

def rgb(r, g, b):
    return pygame.Color(r, g, b) # makes life easier!


def drawText(environment, msg, x, y, size):
    fontObj = pygame.font.Font('freesansbold.ttf', size)
    msgSurfaceObj = fontObj.render(msg, False, rgb(255, 255, 255))
    environment.blit(msgSurfaceObj, (x, y))
