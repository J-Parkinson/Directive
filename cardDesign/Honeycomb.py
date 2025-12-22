from random import randint, random
import turtle
from math import sqrt, cos, sin

from Bounds import Bounds

def randbool():
    return bool(randint(0, 1))

def halfHexagon(center, sideLength):
    startLocation = (center[0] + sideLength / 2, center[1] - (sideLength * sqrt(3) / 2))
    turtle.penup()
    turtle.goto(*startLocation)
    turtle.pendown()
    turtle.setheading(60)
    turtle.forward(sideLength)
    for i in range(2):
        turtle.left(60)
        turtle.forward(sideLength)

def wiringHead(center, headSize, overlapDetails, start):
    if (overlapDetails[0]):
        turtle.left(60 * (randint(0, 1) * 2 - 1))
        return randint(0,1) == 1

    #Initial setup
    isPenDown = turtle.isdown()
    turtle.penup()
    turtle.goto(*center)

    # Circle
    turtle.back(headSize)
    turtle.right(90)
    turtle.pendown()
    turtle.circle(headSize)
    turtle.left(90)
    turtle.penup()
    turtle.forward(headSize)

    if not start:
        # Rotate randomly by 60 degrees and continue
        turtle.left(60 * (randint(0,1) * 2 - 1))
    turtle.forward(headSize)

    if (isPenDown):
        turtle.pendown()

    return randint(0,1) == 0

def addWiring(center, sideLength, overlapDetails, probability=1):
    hadHead = False
    headSize = sideLength/7

    if (probability == 1):
        # Start of wiring - we're not overlapping
        # Choose a wiring head, use that
        wiringHead(center, headSize, overlapDetails, True)
        hadHead = True
    else:
        addHead = random() > probability

        if addHead:
            # Line might finish - calculate head + done?
            canContinue = wiringHead(center, headSize, overlapDetails, False)
            if not canContinue:
                return

            hadHead = True
            probability = sqrt(probability)
        else:
            turtle.pendown()
            turtle.back(headSize)
            turtle.penup()
            turtle.forward(headSize)

    probability *= 0.85
    # Move in direction given by function

    turtle.pendown()
    turtle.forward((sideLength * 2) - (headSize*2))
    if (not hadHead):
        turtle.forward(headSize)

    turtle.penup()
    turtle.forward(headSize)

    position = turtle.pos()
    turtle.back(headSize)

    overlapDetails = [not overlapDetails[0] if overlapDetails[1] else overlapDetails[0], overlapDetails[1]]

    addWiring(position, sideLength, overlapDetails, probability)

def calculateHoneycombCenters(center, sideLength, bounds):
    offsets = (sideLength*3, sideLength*sqrt(3))

    width = int((bounds.xMax - bounds.xMin)//(sideLength*3) + 2)
    height = int((bounds.yMax - bounds.yMin)//(sideLength*sqrt(3)) + 2)

    def calculateCenters(offset, center, number):
        iRange = [x * offset for x in range(number)]
        maxIRange = max(iRange)
        iRange = [x - (maxIRange/2) + center for x in iRange]
        return iRange

    iRange = calculateCenters(offsets[0], center[0] - (offsets[0]/4), width)
    i2Range = calculateCenters(offsets[0], center[0] + (offsets[0]/4), width)
    jRange = calculateCenters(offsets[1]/2, center[1], height*2)

    centers = [(i,j) for i in iRange for j in jRange[::2]] + [(i,j) for i in i2Range for j in jRange[1::2]]

    return centers

def Honeycomb(self, center, sideLength, bounds):
    centers = calculateHoneycombCenters(center, sideLength, bounds)

    for center in centers:
        halfHexagon(center, sideLength)

    return (centers, sideLength)

def HoneycombWiring(self, centers, sideLength, density=None):
    density = density or 1
    for i in range(int(sqrt(len(centers)) * density)):
        centerToUse = centers[randint(0, len(centers) - 1)]
        # We can use either the center exactly,
        # or use one of the 6 points equidistant from the midpoint of the hexagon line and the center
        # or use one of the 6 points equidistant from the end of the hexagon line and the center
        # We triple the odds of the center since it looks nice
        whichToUse = randint(0,4)
        angleForWiring = randint(0,5) * 60
        if (whichToUse < 2):
            # midpoint
            distanceFromCenter = sideLength * sqrt(3) / 4
            angleFromCenter = randint(0,5)*60 + 30
            xDelta = cos(angleFromCenter) * distanceFromCenter
            yDelta = sin(angleFromCenter) * distanceFromCenter
            center = [centerToUse[0] + xDelta, centerToUse[1] + yDelta]
            overlapsLine = (False, False)
        elif (whichToUse < 4):
            # end
            distanceFromCenter = sideLength / 2
            angleFromCenter = randint(0, 5) * 60
            xDelta = cos(angleFromCenter) * distanceFromCenter
            yDelta = sin(angleFromCenter) * distanceFromCenter
            center = [centerToUse[0] + xDelta, centerToUse[1] + yDelta]
            overlapsLine = (False, (angleForWiring % 180) == (angleFromCenter % 180))
        else:
            # center
            center = centerToUse
            overlapsLine = (False, True)

            #TODO :FIX THE DAMN CENTRE LOGIC - THE CIRCLES DON'T ALIGN
        angleForWiring = randint(0,5)*60
        turtle.setheading(angleForWiring)
        turtle.penup()
        turtle.goto(*center)

        addWiring(center, sideLength, overlapsLine)

turtle.Turtle.honeycomb = Honeycomb
turtle.Turtle.addwiring = HoneycombWiring

# --- Main Execution Block ---
if __name__ == '__main__':
    # 1. Setup Screen
    screen = turtle.Screen()
    screen.setup(width=800, height=1000)
    screen.title("Extension Method Example")

    turtle.hideturtle()
    turtle.tracer(False)

    t = turtle.Turtle()
    t.speed(100)

    with Bounds(600, 960) as bounds:
        honeycomb = t.honeycomb((0,0), 36, bounds)
        t.boundingbox(30)
        t.addwiring(*honeycomb)
    turtle.done()