## Todd And Daves 'Circles'

import time
import random
from graphics import *
from threading import *

s = Semaphore() # implements mutal exclusion

class Circle:
    # circle class - the digital organism itself
    # phenotypes are attributes, eg: speed, vision...
    def __init__(self, spawn, environment):
        self.spawn = spawn
        self.body = Circle(spawn, 10) # radius is 10 from now
        self.alive = True # turns false when dead

    def run(self, environment):
        self.body.draw(enviroment)
        # while self.alive:
            # take in inputs
            # do some thinking
            # move
            

class Chromosome:
    # chromosome class, every circle has one!
    # chromosome contains lots genes, which change over generations
    # genome is fixed length, made of one chromosome
    def __init__(self, genome):
        self.genome = genome # array of genes

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
        
        
        
    
            
def createEnvironment():
    environment = GraphWin("Circles", 800, 600)
    statBarrier = Line(Point(600, 0), Point(600, 600))
    statBarrier.draw(environment)

    return environment
    

def main():
    environment = createEnvironment()

main()
