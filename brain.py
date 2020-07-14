import numpy as np
import random

class Brain:


    def __init__(self, brain = None, size = 700):
        self.directions = np.zeros((size,  2))
        if(brain == None):
            for i in range(size):
                for j in range(2):
                    self.directions[i, j] = random.randint(-5, 5)
        else:
            for i in range(size):
                for j in range(2):
                    self.directions[i, j] = brain.getDirections()[i, j]

    def getDirection(self, index):
        return self.directions[index, :]

    def getDirections(self):
        return self.directions

    def setDirections(self, directions):
        self.directions = directions

    def mutate(self, size, bounce):
        for x in range(size):
            for y in range(2):
                dice = random.randint(0, bounce)
                if(dice == 0):
                    self.directions[x, y] = random.randint(-5, 5)

    def mergeBrains(self, secondBrain):
        firstSize = self.getDirections().__len__()
        secondSize = secondBrain.getDirections().__len__()
        firstDir = self.getDirections()
        secondDir = secondBrain.getDirections()
        mergedDir = np.zeros((firstSize + secondSize, 2))

        for i in range(firstSize):
            for j in range(2):
                mergedDir[i, j] = firstDir[i, j]
        for i in range(secondSize):
            for j in range(2):
                mergedDir[firstSize + i, j] = secondDir[i, j]

        mergedBrain = Brain(size=firstSize + secondSize)
        mergedBrain.setDirections(mergedDir)
        return mergedBrain