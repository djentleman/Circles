#library imports
import time
import random
import math
from threading import *


class Chromosome:
    # chromosome class, every circle has one!
    # chromosome contains lots genes, which change over generations
    # genome is fixed length, made of one chromosome
    def __init__(self, genome):
        self.genome = genome # array of genotypes
        # where are the genes :S? 
    def displayGenome(self):
        print(self.genome)


    def getGene(self, index):
        return (self.genome[index])

    def mutate(self):
        # pick random gene
        genomeSize = len(self.genome)
        geneToChange = random.randint(0, genomeSize - 1)
        self.genome[geneToChange].mutate()

class Gene:
    # gene, consists of a name and genotype (AA/Aa/aA/aa),
    # and a phenotype it is tied to
    #genotype is expressed a boolean tuple
    
    def __init__(self, name, phenotype, dominant):
        self.name = name # eg. long legged
        self.phenotype = phenotype # what it affects; how much it affects
        self.dominant = dominant
        # store allele here!
        # is left for the organism code to decide

    def mutate(self):
        rand = random.random() # generate float between 1 and 0
        if rand > 0.99:
            # effect phenotype
            print()
        else:
            # effect genotype
            genoRand1 = random.randint(0,1)
            genoRand2 = random.randint(0,1)
            
def generateRandomChromosome(genes):

    genome = []
    
    for i in range(len(genes)):
        geneL1 = random.randint(0,1)
        geneL2 = random.randint(0,1)
        genome.append((geneL1, geneL2))

    return Chromosome(genome)
        
        
def breed (parent1, parent2, genomeLength):
    newGenome = []
    for i in range(genomeLength): 
        newGene = punnett(parent1.getGene(i), parent2.getGene(i))
        newGenome.append(newGene)
    return(newGenome)
        
def punnett(g1, g2):

    sections = []
    sections.append((g1[0], g2[0]))
    sections.append((g1[0], g2[1]))
    sections.append((g1[1], g2[0]))
    sections.append((g1[1], g2[1]))

    sectionToChoose = random.randint(0, 3)
    return (sections[sectionToChoose])


def generateGenes():
    geneIndex = []
    gene = Gene("speed gene 1", ["speedCooeficiant"], True) # s = (m.n) + c
    geneIndex.append(gene) # AA/Aa/aA = 0.9 aa = 0.4
    gene = Gene("speed gene 2", ["speedCooeficiant"], True)
    geneIndex.append(gene)
    gene = Gene("speed gene 3", ["speedConstant"], True)
    geneIndex.append(gene) # AA/Aa/aA = 0.4 aa = 0.0
    

    return geneIndex
