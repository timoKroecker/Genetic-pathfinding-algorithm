import time
import random
import numpy as np
from graphics import *
from dot import *

north = 0
east = 1
south = 2
west = 3
winPos = (1200, 25)

dotNum = 100
steps = 400
speed = 0.01
gens = 4000
era_size = 25
width = 500
height = 900
framewidth = 20

goalX = width / 2 + framewidth
goalY = framewidth

maxDotSpeed = 5



def main(isVisual):

    borders, lines, dots = initialization()

    if(isVisual):
        multiDotShow(1, dots, borders, lines, steps // 2)
        for i in range(gens):
            champ = fittestDot(dots)
            dots = []
            for j in range(dotNum):
                dots.append(Dot(width, height, framewidth, brain=champ.getBrain(), steps=steps))
                if(not j == 0):
                    dots[j].getBrain().mutate(steps, bounce=random.randint(1, 10))
            if(i + 2 > 20):
                multiDotShow(i + 2, dots, borders, lines, steps)
            else:
                multiDotShow(i + 2, dots, borders, lines, steps // 2)
    else:
        hiddenDotShow(0, dots, borders, lines, steps)
        mutationBounce = 0
        for i in range(gens + 1):
            champ = fittestDot(dots)
            print(  "Gen: " + str(i) + " Steps: " + str(champ.getSteps()) + 
                    " Distance: %.2f" % champ.getDistance(goalX, goalY) + 
                    " Fitness: %.2f" % champ.getFitness() + 
                    " Mutation_Rates: 1/" + str(mutationBounce + 1))
            resetAll(dots, steps)
            if((i + 1) % era_size == 1):
                champShow(champ, lines, borders, steps)
                champ.calculateFitness(goalX, goalY)
                print("Era " + str((i // era_size) + 1))
                champ.reset(steps, width, height, framewidth)
            dots = []
            for j in range(dotNum):
                dots.append(Dot(width, height, framewidth, brain=champ.getBrain(), steps=steps))
                if(not j == 0):
                    mutationBounce = bounce=random.randint(1, 25)
                    dots[j].getBrain().mutate(steps, mutationBounce)
            hiddenDotShow(i + 2, dots, borders, lines, steps)




def initialization():
    borders = np.zeros((4, 4))
    lines = []
    dots = []

    borders[0] = [framewidth + height / 4 - 2 * maxDotSpeed, framewidth + width, framewidth + height / 4, framewidth + width / 3]
    borders[1] = [framewidth + height * 3 / 4 - 2 * maxDotSpeed, framewidth + 2 / 3 * width, framewidth + height * 3 / 4, framewidth]

    lines.append(Line(Point(0, framewidth), Point(width + 2 * framewidth, framewidth)))
    lines.append(Line(Point(0, height + framewidth), Point(width + 2 * framewidth, height + framewidth)))
    lines.append(Line(Point(framewidth, 0), Point(framewidth, height + 2 * framewidth)))
    lines.append(Line(Point(width + framewidth, 0), Point(width + framewidth, height + 2 * framewidth)))

    for i in range(2):
        lines.append(Line(Point(borders[i, west], borders[i, south]), Point(borders[i, east], borders[i, south])))
        lines.append(Line(Point(borders[i, west], borders[i, north]), Point(borders[i, east], borders[i, north])))
        lines.append(Line(Point(borders[i, west], borders[i, south]), Point(borders[i, west], borders[i, north])))
        lines.append(Line(Point(borders[i, east], borders[i, south]), Point(borders[i, east], borders[i, north])))

    for i in range(dotNum):
        dots.append(Dot(width, height, framewidth, steps=steps))
    
    return borders, lines, dots


def champShow(dot, lines, borders, currentSteps):

    win = GraphWin("champShow", width + 2 * framewidth, height + 2 * framewidth)
    win.setBackground(color_rgb(100, 100, 100))
    win.master.geometry('%dx%d+%d+%d' % (width + 2 * framewidth, height + 2 * framewidth, winPos[0], winPos[1]))

    drawTheLines(win, lines)

    goal = Circle(Point(goalX, goalY), 5)
    goal.setFill(color_rgb(0, 255, 0))
    goal.draw(win)

    circle = Circle(dot.getPoint(), 3)
    circle.setFill(color_rgb(0, 0, 0))
    circle.draw(win)

    headline = Text(Point(110, 10), "ChampShow - Step: 0")
    headline.draw(win)

    time.sleep(1)

    headline.undraw()

    for x in range(currentSteps):
        #print(x)
        headline = Text(Point(110, 10), "ChampShow - Step: {0}".format(x))
        headline.draw(win)

        if(dot.isAlive() and not dot.isWinner()):
            time.sleep(3 * speed)
            circle.undraw()
            dot.move(x, maxDotSpeed)
            if(crashedFrame(dot) or crashedObstacle(dot, borders)):
                #dot.setToPrevPosition()
                dot.kill(x)
            if(reachedGoal(dot)):
                dot.makeWinner(x)
            circle = Circle(dot.getPoint(), 3)
            circle.setFill(color_rgb(0, 0, 0))
            circle.draw(win)
        headline.undraw()

    win.close()

def hiddenDotShow(wave, dots, borders, lines, currentSteps):
    noWinnerYet = True
    for x in range(currentSteps):
        if(noWinnerYet and not allDead(dots)):
            for y in range(dotNum):
                if(dots[y].isAlive() and not dots[y].isWinner()):
                    dots[y].move(x, maxDotSpeed)
                    if(crashedFrame(dots[y]) or crashedObstacle(dots[y], borders)):
                        #dots[y].setToPrevPosition()
                        dots[y].kill(x)
                    if(reachedGoal(dots[y])):
                        dots[y].makeWinner(x)
                        noWinnerYet = False
    for y in range(dotNum):
        dots[y].calculateFitness(goalX, goalY)

        
def multiDotShow(wave, dots, borders, lines, currentSteps):

    noWinnerYet = True

    win = GraphWin("multiDotShow", width + 2 * framewidth, height + 2 * framewidth)
    win.setBackground(color_rgb(100, 100, 100))
    win.master.geometry('%dx%d+%d+%d' % (width + 2 * framewidth, height + 2 * framewidth, winPos[0], winPos[1]))

    drawTheLines(win, lines)

    goal = Circle(Point(goalX, goalY), 5)
    goal.setFill(color_rgb(0, 255, 0))
    goal.draw(win)

    circles = []
    for y in range(dotNum):
        circles.append(Circle(dots[y].getPoint(), 3))
        circles[y].setFill(color_rgb(0, 0, 0))
        circles[y].draw(win)

    headline = Text(Point(110, 10), "Wave: {0} Steps: 0".format(wave))
    headline.draw(win)

    time.sleep(1)

    headline.undraw()

    for x in range(currentSteps):
        if(noWinnerYet):
            print(x)
            string = "Wave: {0} Step: {1}".format(wave, x)
            headline = Text(Point(110, 10), string)
            headline.draw(win)

            for y in range(dotNum):
                if(dots[y].isAlive() and not dots[y].isWinner()):
                    time.sleep(speed / dotNum)
                    circles[y].undraw()
                    dots[y].move(x, maxDotSpeed)
                    circles[y] = Circle(dots[y].getPoint(), 3)
                    if(crashedFrame(dots[y]) or crashedObstacle(dots[y], borders)):
                        dots[y].setToPrevPosition()
                    if(reachedGoal(dots[y])):
                        dots[y].makeWinner(x)
                        noWinnerYet = False
                    if(y == 0):
                        circles[y].setFill(color_rgb(255, 0, 0))
                    else:
                        circles[y].setFill(color_rgb(0, 0, 0))
                    circles[y].draw(win)
            headline.undraw()
    for y in range(dotNum):
        dots[y].calculateFitness(goalX, goalY)
    
    win.close()

def crashedFrame(dot, puffer = 3):
    x = dot.getX()
    y = dot.getY()
    frame = (x <= framewidth + puffer) or (y <= framewidth + puffer) or (x >= framewidth + width - puffer) or (y >= framewidth + height - puffer)
    return frame

def crashedObstacle(dot, borders, puffer = 3):
    x = dot.getX()
    y = dot.getY()
    border0 = (borders[0, west] - puffer <= x) and (x <= borders[0, east] + puffer) and (borders[0, north] - puffer <= y) and (y <= borders[0, south] + puffer)
    border1 = (borders[1, west] - puffer <= x) and (x <= borders[1, east] + puffer) and (borders[1, north] - puffer <= y) and (y <= borders[1, south] + puffer)
    border2 = (borders[2, west] - puffer <= x) and (x <= borders[2, east] + puffer) and (borders[2, north] - puffer <= y) and (y <= borders[2, south] + puffer)
    border3 = (borders[3, west] - puffer <= x) and (x <= borders[3, east] + puffer) and (borders[3, north] - puffer <= y) and (y <= borders[3, south] + puffer)
    return border0 or border1 or border2 or border3

def reachedGoal(dot):
    return dot.x >= goalX - 8 and dot.x <= goalX + 8 and dot.y >= goalY - 8 and dot.y <= goalY + 8

def livingDots(dots):
    output = []
    for dot in dots:
        if(dot.isAlive()):
            output.append(dot)
    if(output.__len__() == 0):
        return None
    return output

def closestDotAlive(dots):
    return closestDot(livingDots(dots))

def closestDot(dots):
    bestDistance = height
    closestDot = None
    if(dots == None):
        return None
    for i in range(dots.__len__()):
        iDistance = dots[i].getDistance(goalX, goalY)
        if(iDistance < bestDistance):
            bestDistance = iDistance
            closestDot = dots[i]
    return closestDot

def isCloserThan(dot1, dot2):
    return dot1.getDistance(goalX, goalY) < dot2.getDistance(goalX, goalY)


def fittestDotIndex(dots):
    bestFitness = -20000
    bestDotIndex = 0
    for x in range(dotNum):
        if(dots[x].getFitness() > bestFitness):
            bestFitness = dots[x].getFitness()
            bestDotIndex = x
    return bestDotIndex

def fittestDot(dots):
    if(allDead(dots)):
        return lastManStanding(dots)
    else:
        return dots[fittestDotIndex(dots)]

def allDead(dots):
    output = True
    for dot in dots:
        if(dot.isAlive()):
            output = False
    return output

def lastManStanding(dots):
    mostSteps = 0
    lastDot = None
    for dot in dots:
        if(mostSteps < dot.getSteps()):
            mostSteps = dot.getSteps()
            lastDot = dot
    return lastDot

def drawTheLines(win, lines):
    for line in lines:
        line.draw(win)

def mergeAllBrains(brains):
    outputBrain = brains[0].mergeBrains(brains[1])
    for i in range(brains.__len__() - 2):
        outputBrain = outputBrain.mergeBrains(brains[i + 2])
    return outputBrain

def resetAll(dots, steps):
    for dot in dots:
        dot.reset(steps, width, height, framewidth)


main(False)