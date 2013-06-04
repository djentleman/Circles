## Todd And Daves 'Circles'

import time
import random
from graphics import *
from threading import *

s = Semaphore() # implements mutal exclusion

class Organism:
    # circle class - the digital organism itself
    # phenotypes are attributes, eg: speed, vision...
    # every organism has
    def __init__(self, spawn, environment):
        self.spawn = spawn
        self.body = Circle(spawn, 10) # radius is 10 from now
        self.alive = True # turns false when dead
        self.environment = environment
        
        genderSeed = random.random()
        self.isMale = False
        if genderSeed > 0.5: # weighting will be decided in genome
            self.isMale = True # 50% chance of being male for now
            
        self.aggressionIndex = random.randint(0, 255)
        # aggression will be determined in genome (and hunger), with some random element
        # random for now
        
        
        

    def run(self):
        self.body.draw(self.environment)
        self.getColor()
        # while self.alive:
        # take in inputs
        # do some thinking
        # move

    def getColor(self):
        # color is defined by gender and aggression
        self.body.setOutline(color_rgb(self.aggressionIndex, 0, 0)) # more red when aggressive
        self.body.setFill("pink")
        if self.isMale:
            self.body.setFill("blue")
        
            

class Chromosome:
    # chromosome class, every circle has one!
    # chromosome contains lots genes, which change over generations
    # genome is fixed length, made of one chromosome
    def __init__(self, genome):
        self.genome = genome # array of genes

    def mutate(self):
        # pick random gene
        genomeSize = len(self.genome)
        geneToChange = random.randint(0, genomeSize - 1)
        self.genome[geneToChange].mutate()

class Gene:
    # gene, consists of a name and genotype (AA/Aa/aA/aa),
    # and a phenotype it is tied to
    #genotype is expressed a boolean tuple
    
    def __init__(self, name, genotype, phenotype):
        self.name = name # eg. long legged
        self.genotype = genotype # eg. (False, True) - aA
        self.phenotype = phenotype # an array of everything this
        # gene effects, and how much it effects it, stored as tuples
        # eg. [("speed", 1.1), ("HP", 0.95), ...., ]

    def mutate(self):
        rand = random.random() # generate float between 1 and 0
        if rand > 0.99:
            # effect phenotype
            print()
        else:
            # effect genotype
            genoRand1 = random.randint(0,1)
            genoRand2 = random.randint(0,1)
            self.genotype = (bool(genoRand1), bool(genoRand2))
            
        
        
        

def getLine(point1, point2):
    line = Line(point1, point2)
    line.setFill("white")
    return line

def drawButton(environment, contents, xCoord, yCoord):
    # all buttons 30 by 30
    button = Rectangle(Point(xCoord - 15, yCoord - 15), Point(xCoord + 15, yCoord + 15))
    button.setOutline("white")
    text = Text(Point(xCoord, yCoord), contents)
    text.setFill("white")
    button.draw(environment)
    text.draw(environment)
    

def drawInterface(environment):

        
    statBarrier = getLine(Point(750, 0), Point(750, 751))
    statBarrier.draw(environment)

    controlBarrier = getLine(Point(750, 600), Point(1050, 600))
    controlBarrier.draw(environment)
    
    lblStats = Text(Point(900, 50), "STATS")
    lblStats.setFill("white")
    lblStats.draw(environment)

    drawButton(environment, "«", 850, 700)
    drawButton(environment, "►", 900, 700)
    drawButton(environment, "»", 950, 700)
    
    
            
def createEnvironment():
    environment = GraphWin("Circles", 1050, 750)
    environment.setBackground("black")
    
    # RANDOMLY GENERATE FOOD

    drawInterface(environment)

    return environment

def test(environment):
    organism1 = Organism(Point(100, 100), environment)
    organism2 = Organism(Point(100, 200), environment)
    organism3 = Organism(Point(300, 200), environment)
    organism1.run()
    organism2.run()
    organism3.run()
    

def main():
    environment = createEnvironment()
    test(environment)

    # render the environment, then wait for clicks

main()
