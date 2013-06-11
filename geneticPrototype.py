import random
geneIndex = []


class Chromosome:
    # chromosome class, every circle has one!
    # chromosome contains lots genes, which change over generations
    # genome is fixed length, made of one chromosome
    def __init__(self, genome):
        self.genome = genome # array of genoTYPES!!!

    def displayGenome(self):
        print(self.genome)

    def getGenomeLength(self):
        return (len(self.genome))

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
    
    def __init__(self, name, phenotype):
        self.name = name # eg. long legged
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
            
def main():
    genomeLength = generateGenes()
    organisms = []
    numberOfOrganisms = int(input("How many organisms in this simulation?"))

    for i in range(numberOfOrganisms):
        genome = []
        
        for i in range(genomeLength):
            geneL1 = random.randint(1,2)
            geneL2 = random.randint(1,2)
            genome.append((geneL1, geneL2))

        newChrom = Chromosome(genome)
        organisms.append(newChrom)

    print("GENETIC PROTOTYPE")
    print("-----------------")
    print("Here are the initial genesequences")


    while True:
        
        for i in range(len(organisms)):
            print("gene", i, ":")
            organisms[i].displayGenome()
            
        parent1 = int(input("which parent would you like to select for breeding first"))
        parent2 = int(input("which parent would you like to select for breeding second"))
        childGenome = breed(organisms[parent1], organisms[parent2], genomeLength)
        child = Chromosome(childGenome)
        child.displayGenome()
        organisms.append(child)
        
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
    gene = Gene("gene1", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene2", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene3", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene4", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene5", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene6", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene7", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene8", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene9", [("speed", 10)])
    geneIndex.append(gene)
    gene = Gene("gene10", [("speed", 10), ("radius", 5)])
    geneIndex.append(gene)

    return len(geneIndex)
