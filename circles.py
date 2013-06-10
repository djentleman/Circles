## Todd And Daves 'Circles'



# local imports
from food import *
from genetics import *
from interface import *


# library imports
import time
import random
import math
from graphics import *
from threading import *


s = Semaphore() # implements mutal exclusion
speedMult = 1 # speed multiplier - global (for now)




class Organism:
    # circle class - the digital organism itself
    # phenotypes are attributes, eg: speed, vision...
    # ultimatley each organism will be running on a seperate thread
    def __init__(self, spawn, environment):
        self.spawn = spawn
        self.radius = (random.random() * 6) + 1  # radius is random for now
        self.mass = math.pi * (self.radius * self.radius) # area
        self.surfaceArea = 2 * math.pi * self.radius
        self.energy = random.randint(80, 120) # start off at ~100 energy (ultimatley this will be determined in genome)
        # everything uses energy, having keen vision saps energy more than awful vision
        # this is effectivley the thing that drives the organisms, energy can be gained
        # by eating food, or other organisms
        self.activity = "wonder" #the organism is currently 'doing' something
        self.body = Circle(spawn, self.radius)
        self.alive = True # turns false when dead
        self.environment = environment
        self.speed = random.random() / 2 #will be decided in genome
        self.direction = random.randint(1, 360)
        self.visionRadius = random.randint(20, 90)
        self.visionDistance = random.randint(50, 200)
        self.focused = False # focused organisms have stats on display
        genderSeed = random.random()
        self.isMale = False
        if genderSeed > 0.5: # weighting will be decided in genome
            self.isMale = True # 50% chance of being male for now
            
        aggRand1 = random.randint(1, int(120 ** 0.5)) # start off with max agression
        aggRand2 = random.randint(1, int(120 ** 0.5)) # as 120, changes with hunger
        self.aggressionIndex = aggRand1 * aggRand2 # produces bell curve
        self.aggression = float(self.aggressionIndex) # float version of agression index
        # aggression will be determined in genome (and hunger), with some random element
        # random for now
    
    def focus(self):
        self.body.setOutline("green")
        self.focused = True

    def unfocus(self):
        self.body.setOutline(color_rgb(self.aggressionIndex, 0, 0))
        self.focused = False
                

    def set(self):
        self.body.draw(self.environment)
        self.getColor()

    def move(self):
        start = self.energy
        
        # looks at surroundings, then does something
        self.look(organisms)
        # THINKING GOES HERE
        
        success = self.wander()

        
        if not success: # not success = nothing happened
            # sap some energy for idling
            self.energy -= 0.0005


                        
        end = self.energy
        energyChange = end - start
        # change aggression based on energy change

        # if energy increases, agression decreases
        # therefore, change in aggression is protional to -change in energy
        oldAggression = self.aggressionIndex
        
        self.aggression += (-energyChange)
        self.aggressionIndex = int(self.aggression)

        newAggression = self.aggressionIndex
        
        if self.aggressionIndex > 255:
            self.aggressionIndex = 255
        elif self.aggressionIndex < 1:
            self.aggressionIndex = 1 # stops hex color from crashing

        # update outline colour here (unless it's green)
        if newAggression != oldAggression:
            # colour has changed
            if not self.focused:
                # cant be focused (green)
                self.body.setOutline(color_rgb(self.aggressionIndex, 0, 0))

        if self.energy <= 0:
            self.alive = False
            self.body.setOutline("brown4")
            self.body.setFill("brown4")

        return self.alive # returns if the organism is alive

    def moveTowards(self, angle):
        self.direction = angle
        centerPoint = self.body.getCenter()
        circleX = centerPoint.getX()
        circleY = centerPoint.getY()
        if circleX == food.x and circleY == food.y:
            print("got the food!")
        
              

    def look(self, organisms):
        centerPoint = self.body.getCenter()
        circleX = centerPoint.getX()
        circleY = centerPoint.getY()
        for index in range(len(food) - 1):
            current = food[index]
            iX = current.x
            iY = current.y
            distX = circleX - (iX - current.radius)
            distY = circleY - (iY - current.radius)

            distance = math.hypot(distX, distY)
            angleTo = math.degrees(math.atan2(distY, distX))

            angleTo += 180
            angleTo = math.radians(angleTo)

            if self.direction < 0:
                self.direction += 360
            radiusRadians = math.radians(self.visionRadius)
            directionRadians = math.radians(self.direction)

            if distance <= self.visionDistance and (angleTo >= directionRadians - (radiusRadians/2)) and (angleTo <= directionRadians + (radiusRadians/2)):
                self.moveTowards(math.degrees(angleTo), food[index])
                if self.focused == True:
                    print("found food")


        #find other organisms
        for i in range(len(organisms) - 1): 
            iCenter = organisms[i].body.getCenter()
            iX = iCenter.getX()
            iY = iCenter.getY()
            if iX != circleX and iY != circleY:
                distX = circleX-iX
                distY = circleY-iY
                
                distance = math.hypot(distX, distY)#find the hypotenuse
                angleTo = math.degrees(math.atan2(distY, distX)) # find angle between circles
                
                angleTo += 180
                angleTo = math.radians(angleTo)
                #if (distY < 0):
                #   angleTo = angleTo + math.pi
                if self.direction < 0:
                    self.direction += 360
                radiusRadians = math.radians(self.visionRadius)
                directionRadians = math.radians(self.direction)
                #print(self.direction)

                if self.focused == True:                 
                    visionTriangleLeftX = circleX + (self.visionDistance * math.cos(directionRadians + (radiusRadians / 2)))
                    visionTriangleLeftY = circleY + (self.visionDistance * math.sin(directionRadians + (radiusRadians / 2)))
                    visionTriangleRightX = circleX + (self.visionDistance * math.cos(directionRadians - (radiusRadians / 2)))
                    visionTriangleRightY = circleY + (self.visionDistance * math.sin(directionRadians - (radiusRadians / 2)))
                    visionTriangle = Polygon(Point(circleX,circleY), Point(visionTriangleLeftX, visionTriangleLeftY), Point(visionTriangleRightX, visionTriangleRightY))
                    visionTriangle.setFill("white")
                    visionTriangle.draw(self.environment)
                    visionTriangle.undraw()

                    # update sight reticule
                    
                #if distance <= self.visionDistance and (angleTo >= directionRadians - (radiusRadians/2)) and (angleTo <= directionRadians + (radiusRadians/2)):
                    #organism has been spotted
                    #if self.focused == True:
                        #organisms[i].focused = True
                    #    print("spotted")
                    #    print(i)
                            
        

    def changeDirection(self, change):
        # energy turning is protpotional to the surface area
        # and the angle being turned
        # it will be taken as mθ, and a multiplier, Δ
        # e(t) = Δ(2πr)|πθ/180| = Δs|πθ/180|
        energyToSap = 0.005 * self.surfaceArea * abs((change * math.pi) / 180)
        if self.energy > energyToSap: # sufficent energy avilable
            self.direction += change
            self.energy -= energyToSap
            return True
        return False
        
            

    def wander(self): # returns if successful
        # wandering saps energy, the larger the mass, the more energy sapped
        # energy (kinetic) can be measured by (mv^2)/2
        # but that would sap too much, so well use a multiplyer, Δ
        # e(w) = (Δ(πr^2)v^2)/2 = (Δmv^2)/2
        global speedMult
        speed = self.speed * speedMult
        # calculate energy to sap
        energyToSap = (0.005 * self.mass * (self.speed * self.speed)) / 2 # Δ is taken as 0.005
        if self.energy > energyToSap: # sufficent energy avilable
            try:
                #print(self.direction)
                self.energy -= energyToSap
                angleRadians = self.direction * ((math.pi) / 180)
                xMovement = speed * math.cos(angleRadians)
                yMovement = speed * math.sin(angleRadians)
                self.body.move(xMovement, yMovement)
                position = self.body.getCenter()
                if position.getX() <= 5 or position.getX() >= 745:
                    xMovement = -xMovement
                    #print("X Movement: ", xMovement)
                    #print("Y Movement: ", yMovement)
                    #print("X Coord: ", position.getX())
                    #print("Y Coord: ", position.getY())
                    #print("-------------x-----------------")
                    #print("-------------------------------")
                    #print("-------------------------------")
                    
                elif position.getY() <= 5 or position.getY() >= 745:
                    yMovement = -yMovement
                    #print("X Movement: ", xMovement)
                    #print("Y Movement: ", yMovement)
                    #print("X Coord: ", position.getX())
                    #print("Y Coord: ", position.getY())
                    #print("-------------y-----------------")
                    #print("-------------------------------")
                    #print("-------------------------------")
                    
                
                newDirection = math.atan2(yMovement, xMovement)
                self.direction = (180 * newDirection) / math.pi
                return True
                
            except(Exception):
                #do nothing
                print("err")
        return False
            
        
    def getColor(self):
        # color is defined by gender and aggression
        self.body.setOutline(color_rgb(self.aggressionIndex, 0, 0)) # more red when aggressive
        self.body.setFill("pink3")
        if self.isMale:
            self.body.setFill("blue")


    




def searchForOrganism(x, y, organisms, stats):
    resetColours(organisms) # reset colours
    organism = None
    for current in organisms:
        pos = current.body.getCenter()
        radius = current.body.getRadius()
        if x >= (pos.getX() - radius) and x <= (pos.getX() + radius) and \
           y >= (pos.getY() - radius) and y <= (pos.getY() + radius):
            organism = current
            break # break out of loop
    #update stats
    if organism == None:
        resetLocalStats(stats)
        return organism
    gender = "Female"
    if organism.isMale:
        gender = "Male"
    stats[2].setText(gender)
    stats[3].setText(organism.aggressionIndex)
    stats[4].setText(str("%.3f" % organism.direction) + "°")
    stats[5].setText("%.3f" % organism.speed)
    stats[6].setText("%.3f" % organism.mass)
    stats[7].setText("%.3f" % organism.body.getCenter().getX())
    stats[8].setText("%.3f" % organism.body.getCenter().getY())
    stats[9].setText("%.3f" % organism.energy)
    organism.focus()
    return organism
    
def resetColours(organisms):
    for organism in organisms:
         organism.unfocus()
        
def resetLocalStats(stats):
    for index in range(2, len(stats)):
        stats[index].setText("-")
        

def mouseAction(x, y, running, environment, organisms, stats, organism):
    global speedMult
    # mouse has been pressed
    if (x >= 835 and x <= 865 and y >= 685 and y <= 715):
        # slow down
        #print("slow down pressed")
        speedMult *= 0.5
        if speedMult < 0.03125:
            speedMult = 0.03125 # cap at 0.03125
        return running, organism
    elif (x >= 885 and x <= 915 and y >= 685 and y <= 715):
        # pause/play
        updateButton(running, environment)
        if running:
            # change button to play
            return False, organism
        # change button to pause
        return True, organism
    elif (x >= 935 and x <= 965 and y >= 685 and y <= 715):
        # speed up
        #print("speed up pressed")
        speedMult *= 2
        if speedMult > 64:
            speedMult = 64.0 # cap at 64
        return running, organism
    else:
        organism = searchForOrganism(x, y, organisms, stats)
        # search for organism, update stats
        return running, organism
        
    
            
def createEnvironment():
    environment = GraphWin("Circles", 1050, 750)
    environment.setBackground("black")

    drawInterface(environment)

    return environment

def spawn(environment, n):
    organisms = []
    for i in range(n):
        organism = Organism(Point(100, 100), environment)
        organisms.append(organism)
        organism.set()
    return organisms


def generateFood(environment):
    # generates food in random areas
    # food is all rgb(0, 255, 255) for now
    allFood = []

    numberOfClusters = random.randint(20, 45)
    for i in range(numberOfClusters):
        randX = random.randint(0, 750)
        randY = random.randint(0, 750)
        food = Food(randX, randY, environment)
        allFood.append(food)
        
    return allFood

def growFood(food):
    rand = random.random()
    if rand > 0.95:
        randomFoodID = random.randint(0, len(food) - 1)
        current = food[randomFoodID]
        current.grow()
    

def main():
    global speedMult
    global organisms
    noOfOrganisms = 20
    environment = createEnvironment()
    organisms = spawn(environment, noOfOrganisms)
    global food
    food = generateFood(environment) # food = array of all food
    stats = renderStats(environment) # changable stats are outputted as an array
    count = 0
    organism = None
    running = True
    while True: # organisms don't move when not running
        while running:
            start = time.clock()
            # random food growth
            growFood(food)
            #####################
            #update stats
            stats[0].setText(len(organisms))
            stats[1].setText(str(speedMult) + "x")

            if organism != None and (count % 20 == 0):
                # this is a critical area - only important stats go here
                # modularize this out at some point (it's recycled code)
                stats[3].setText(organism.aggressionIndex)
                stats[4].setText(str("%.3f" % organism.direction) + "°")
                stats[5].setText("%.3f" % organism.speed)
                stats[7].setText("%.3f" % organism.body.getCenter().getX())
                stats[8].setText("%.3f" % organism.body.getCenter().getY())
                stats[9].setText("%.3f" % organism.energy)
            # -----------------
            isAlive = organisms[count % noOfOrganisms].move()
            if not isAlive:
                organisms.remove(organisms[count % noOfOrganisms])
                noOfOrganisms -= 1 # current orgaism has died, leaving a tasty corpse
            count += 1
            # check for mouse clicks
            mouseClick = environment.checkMouse()
            if mouseClick != None: # else continue
                running, organism = mouseAction(mouseClick.getX(), mouseClick.getY(), \
                                                running, environment, organisms, stats, organism)
            end = time.clock()
            timeTaken = end - start # time taken to process 1 organism
            timeTaken *= noOfOrganisms
            fps = 1 / timeTaken
            #print(fps)
            stats[10].setText("%.1f" % fps + "FPS")

            
        stats[1].setText("Paused") # update
        mouseClick = environment.checkMouse()
        if mouseClick != None: # else continue
            running, organism = mouseAction(mouseClick.getX(), mouseClick.getY(), \
                                            running, environment, organisms, stats, organism)
        

main()
