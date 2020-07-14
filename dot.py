import numpy as np
from brain import *
from graphics import *

class Dot:

    def __init__(self, width, height, framewidth, x = None, y = None, velX = None, velY = None, brain = None, steps = 700):
        self.x = x
        self.y = y
        self.prevX = x
        self.prevY = y
        self.vel = np.array([0,0])

        if(x == None):
            self.x = width / 2 + framewidth
            self.prevX = width / 2 + framewidth
        if(y == None):
            self.y = height - 20
            self.prevY = height - 20
        if(not velX == None and not velY == None):
            self.vel = np.array([velX, velY])

        self.brain = Brain(brain=brain, size=steps)
        self.alive = True
        self.winner = False
        self.fitness = 0
        self.steps = steps

    def getPoint(self):
        return Point(self.x, self.y)

    def move(self, index, maxSpeed):
        self.vel[0] = self.vel[0] + self.brain.getDirection(index)[0]
        self.vel[1] = self.vel[1] + self.brain.getDirection(index)[1]

        if(self.vel[0] > maxSpeed):
            self.vel[0] = maxSpeed
        if(self.vel[0] < -maxSpeed):
            self.vel[0] = -maxSpeed
        if(self.vel[1] > maxSpeed):
            self.vel[1] = maxSpeed
        if(self.vel[1] < -maxSpeed):
            self.vel[1] = -maxSpeed

        self.prevX = self.x
        self.prevY = self.y

        self.x = self.x + self.vel[0]
        self.y = self.y + self.vel[1]

    def kill(self, steps):
        self.alive = False

    def isAlive(self):
        return  self.alive

    def makeWinner(self, steps):
        self.winner = True
        self.steps = steps

    def isWinner(self):
        return self.winner

    def getDistance(self, x, y):
        return np.sqrt((self.x - x)**2 + (self.y - y)**2)

    def calculateFitness(self, x, y):
        distance = self.getDistance(x, y)
        if(self.isAlive()):
            if(self.isWinner()):
                self.fitness = 10000 - 10 * self.steps - distance
            else:
                self.fitness = - 10 * self.steps - distance
        else:
            self.fitness = -10000 - 10 * self.steps - distance
            
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPrevX(self):
        return self.prevX

    def getPrevY(self):
        return self.prevY

    def getVel(self):
        return self.vel[0], self.vel[1]

    def getFitness(self):
        return self.fitness

    def getSteps(self):
        return self.steps

    def getBrain(self):
        return self.brain

    def getWinner(self):
        return self.winner

    def setBrain(self, brain):
        self.brain = brain

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setToPrevPosition(self):
        self.x = self.prevX
        self.y = self.prevY

    def reset(self, steps, width, height, framewidth):
        self.x = width / 2 + framewidth
        self.y = height - 20
        self.prevX = width / 2 + framewidth
        self.prevY = height - 20
        self.vel = np.array([0,0])
        self.alive = True
        self.winner = False
        self.steps = steps
        self.fitness = 0


