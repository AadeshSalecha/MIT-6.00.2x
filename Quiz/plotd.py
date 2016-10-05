'''
Author  : Aadesh Salecha
Course  : MIT 6.002x
Date    : Jan 2016
'''
import pylab
import random

class Location(object): 
    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y
        
    def move(self, deltaX, deltaY):
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX, self.y + deltaY)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return (xDist**2 + yDist**2)**0.5
    
    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'

class Field(object):
    def __init__(self):
        self.drunks = None
        
    def addDrunk(self, drunk, loc):
            self.drunk = loc
            
    def moveDrunk(self, drunk):
        currentLocation = self.drunk
        curr_x,curr_y = drunk.takeStep()
        self.drunk = currentLocation.move(curr_x,curr_y)
        
    def getLoc(self, drunk):
        return self.drunk

class Drunk(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name

class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,1.0), (0.0,-1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

def simWalk(field, drunk, numSteps,a):
    pylab.figure(1)
    x_list = []
    y_list = []
    for i in range(numSteps):
        field.moveDrunk(drunk)
        loc = field.getLoc(drunk)
        x_list.append(loc.getX())
        y_list.append(loc.getY())
    
    pylab.plot(x_list,y_list,)
    pylab.title("Walk" + str(a))
    pylab.savefig('Walk' + str(a))
    pylab.close(1)
    return field.getLoc(drunk).getX(), field.getLoc(drunk).getY()

def simManyWalks(field, drunk, numTrials, numSteps):
    average = []
    for i in range(numTrials):
        average.append(simWalk(field,drunk,numSteps,i))
        field.drunk = Location(0,0)
    
    ans_x = 0
    ans_y = 0
    all_x = []
    all_y = []
    
    for i in average:
        all_x.append(i[0])
        all_y.append(i[1])
        ans_x += i[0]
        ans_y += i[1]
    
    pylab.figure("Distances from Origin")
    pylab.title("Distances from Origin",fontsize = 25)
    pylab.plot(all_x,all_y)
    pylab.savefig("Distances from Origin")
    pylab.close("Distances from Origin")
    
    print "Max = ", max(average)
    print "Average x = ",ans_x / numTrials , " Average y = ",ans_y/numTrials


# edit values inthis block of code for different simulations
field = Field()
drunk = UsualDrunk("drunk1")
loc = Location(0,0)
field.addDrunk(drunk,loc)
numTrials = 1000
numSteps = 1000
simManyWalks(field,drunk,numTrials,numSteps)