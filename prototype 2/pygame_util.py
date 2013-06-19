# pygame util
import pygame, sys, time, random, math

def rgb(r, g, b):
    return pygame.Color(r, g, b) # makes life easier!


def drawText(environment, msg, x, y, size):
    drawDimmedText(environment, msg, x, y, size, 255)

def drawDimmedText(environment, msg, x, y, size, dim):
    fontObj = pygame.font.Font('freesansbold.ttf', size)
    msgSurfaceObj = fontObj.render(msg, False, rgb(dim, dim, dim))
    environment.blit(msgSurfaceObj, (x, y))

def drawButton(environment, msg, x, y, width, height):
    # add possible hover/focus animation
    pygame.draw.rect(environment, rgb(255, 255, 255),
                     (x - 20, y - 20, width, height), 1)
    drawText(environment, msg, x - int(width / 5), y - int(height / 4), 18)
    # text positioning needs work

def drawGraphSelect(environment, msg, x, y, width, selected):
    if selected:
        # this box is chosen
        pygame.draw.rect(environment, rgb(255, 255, 255),
                         (x - 45, y - 10, width, 20), 1)
        drawText(environment, msg, x - 40, y - 5, 12)
    else:
        pygame.draw.rect(environment, rgb(160, 160, 160),
                         (x - 45, y - 10, width, 20), 1)
        drawDimmedText(environment, msg, x - 40, y - 5, 12, 160)
