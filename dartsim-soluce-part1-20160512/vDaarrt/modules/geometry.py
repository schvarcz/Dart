'''
@auhtor : Corentin R
@date : February 2015

This file contains geometric objects' constructors. Nothing should be changed
in this file as it would possibly change the comportment of the robot

Modified BenBlop 2016, may 

'''
import math
import pylygon
from numpy import array
from constantes import *


def createSonar(daarrt):

    '''
    return :
        list of pylygon objects containing each sonar of the DAARRT

    arguments :
        daarrt object

    '''

    sonar=[]

    theta = daarrt.sonarAngle*math.pi/180.0


    for i in range(daarrt.nFrontSonar) :

        if daarrt.nFrontSonar>1 :
            x0 = daarrt.robotLenght/2 + 2
            y0 = daarrt.robotWidth*i/(daarrt.nFrontSonar-1) - daarrt.robotWidth/2
        else :
            x0 = daarrt.robotLenght/2 + 2
            y0 = 0

        sonar.append(pylygon.Polygon([(x0,y0),(x0+sonarLenght*math.cos(theta),y0+sonarLenght*math.sin(theta)),(x0+sonarLenght*math.cos(-theta),y0+sonarLenght*math.sin(-theta))]))

    for i in range (daarrt.nBackSonar) :
        if daarrt.nBackSonar >1 :
            x0 = -daarrt.robotLenght/2 + 2
            y0 = daarrt.robotWidth*i/(daarrt.nBackSonar-1) - daarrt.robotWidth/2
        else :
            x0 = -daarrt.robotLenght/2 + 2
            y0 = 0
        sonar.append(pylygon.Polygon([(x0,y0),(-x0-sonarLenght*math.cos(theta),y0+sonarLenght*math.sin(theta)),(-x0-sonarLenght*math.cos(-theta),y0+sonarLenght*math.sin(-theta))]))

    for i in range (daarrt.nLeftSonar):

        if daarrt.nLeftSonar>1 :
            x0 = -daarrt.robotLenght/2 + daarrt.wheelLenght/2 +  (daarrt.robotLenght-daarrt.robotWidth)*i/(daarrt.nLeftSonar-1)
            y0 = -daarrt.robotWidth/2 + 2
        else :
            x0 = 0
            y0=-daarrt.robotWidth/2 + 2

        sonar.append(pylygon.Polygon([(x0,y0),(x0+sonarLenght*math.sin(theta),-y0-sonarLenght*math.cos(theta)),(x0+sonarLenght*math.sin(-theta),-y0-sonarLenght*math.cos(-theta))]))

    for i in range (daarrt.nRightSonar):

        if daarrt.nRightSonar>1 :
            x0 = -daarrt.robotLenght/2 + daarrt.wheelLenght/2 +  (daarrt.robotLenght-daarrt.robotWidth)*i/(daarrt.nLeftSonar-1)
            y0 = daarrt.robotWidth/2 + 2
        else :
            x0 = 0
            y0=daarrt.robotWidth/2 + 2

        sonar.append(pylygon.Polygon([(x0,y0),(x0+sonarLenght*math.sin(theta),+y0+sonarLenght*math.cos(theta)),(x0+sonarLenght*math.sin(-theta),+y0+sonarLenght*math.cos(-theta))]))

    sonar=[poly_translate(poly_rotate(element,daarrt.robotCap),daarrt.posX,daarrt.posY) for element in sonar]

    return sonar

def createBody(daarrt,offsetX,offsetY):

    '''
    return :
        list corresponding to the daarrt's body

    arguments :
        daarrt object
        offsetX : optionnal offset on X axis
        offsetY : optionnal offset on Y axis

    '''

    x0 = offsetX
    y0 = offsetY
    x1 = offsetX + daarrt.robotLenght
    y1 = offsetY
    x2 = offsetX + daarrt.robotLenght
    y2 = offsetY + daarrt.robotWidth
    x3 = offsetX
    y3 = offsetY + daarrt.robotWidth
    body = [(x0,y0) , (x1,y1) , (x2,y2) , (x3,y3)]

    return body
    
    
def createFrontId(daarrt,offsetX,offsetY):

    '''
    return :
        list corresponding to the daarrt's body

    arguments :
        daarrt object
        offsetX : optionnal offset on X axis
        offsetY : optionnal offset on Y axis

    '''

    x0 = offsetX + daarrt.robotLenght/2
    y0 = offsetY
    x1 = offsetX + daarrt.robotLenght
    y1 = offsetY + daarrt.robotWidth/2.01
    x2 = offsetX + daarrt.robotLenght
    y2 = offsetY + daarrt.robotWidth/1.99
    x3 = offsetX + daarrt.robotLenght/2
    y3 = offsetY + daarrt.robotWidth

    frontId = [(x0,y0) , (x1,y1) , (x2,y2), (x3,y3)]

    return frontId

def createWheel(daarrt,offsetX,offsetY):

    '''
    return :
        list corresponding to a daarrt wheel

    arguments :
        daarrt object
        offsetX : optionnal offset on X axis
        offsetY : optionnal offset on Y axis

    '''
    x0 = offsetX
    y0 = offsetY
    x1 = offsetX
    y1 = offsetY - daarrt.wheelWidth
    x2 = offsetX + daarrt.wheelLenght
    y2 = offsetY - daarrt.wheelWidth
    x3 = offsetX + daarrt.wheelLenght
    y3 = offsetY
    wheel=[(x0,y0) , (x1,y1) , (x2,y2) , (x3,y3)]

    return wheel

def createClaw(daarrt,offsetX,offsetY):

    '''
    return :
        list corresponding to the daarrt's claw

    arguments :
        daarrt object
        offsetX : optionnal offset on X axis
        offsetY : optionnal offset on Y axis

    '''

    x0 = offsetX
    y0 = offsetY
    x1 = offsetX + daarrt.clawLenght
    y1 = offsetY
    x2 = offsetX + daarrt.clawLenght
    y2 = offsetY + daarrt.clawWidthClosed/2
    x3 = offsetX
    y3 = offsetY + daarrt.clawWidthClosed/2
    claw = [(x0,y0),(x1,y1),(x2,y2),(x3,y3)]

    return claw

def createClawBase(daarrt,offsetX,offsetY):

    '''
    return :
        list corresponding to the daarrt's clawBase

    arguments :
        daarrt object
        offsetX : optionnal offset on X axis
        offsetY : optionnal offset on Y axis

    '''

    x11 = offsetX
    y11 = offsetY
    x12 = offsetX + daarrt.clawBase
    y12 = offsetY
    x13 = offsetX + daarrt.clawBase
    y13 = offsetY + daarrt.clawWidthClosed
    x14 = offsetX
    y14 = offsetY + daarrt.clawWidthClosed
    clawBase=[(x11,y11),(x12,y12),(x13,y13),(x14,y14)]

    return clawBase

def createRobot(daarrt):

    '''
    return :
        list pylygon object corresponding to the daarrt (wheel )

    arguments :
        daarrt object

    '''

    rotationCenter = [ -daarrt.robotLenght/2 , -daarrt.robotWidth/2 ]

    body = createBody(daarrt , rotationCenter[0] , rotationCenter[1])
    frontId = createFrontId(daarrt , rotationCenter[0] , rotationCenter[1])

    wheel1 = createWheel(daarrt , -daarrt.wheelLenght/2 + rotationCenter[0] , rotationCenter[1])
    wheel2 = createWheel(daarrt , daarrt.robotLenght - daarrt.wheelLenght/2 + rotationCenter[0] , rotationCenter[1])
    wheel3 = createWheel(daarrt , daarrt.robotLenght - daarrt.wheelLenght/2 + rotationCenter[0] , daarrt.robotWidth + daarrt.wheelWidth + rotationCenter[1])
    wheel4 = createWheel(daarrt , -daarrt.wheelLenght/2 + rotationCenter[0] , daarrt.robotWidth + daarrt.wheelWidth + rotationCenter[1])

    clawBase = createClawBase( daarrt , daarrt.robotLenght + rotationCenter[0] , daarrt.robotWidth/2 - daarrt.clawWidthOpened/2 + rotationCenter[1])
    claw1 = createClaw(daarrt , daarrt.robotLenght + daarrt.clawBase + rotationCenter[0] , daarrt.robotWidth/2 - daarrt.clawWidthClosed/2 - daarrt.clawWidthOpened * daarrt.clawOpening/180.0 + rotationCenter[1])
    claw2 = createClaw(daarrt , daarrt.robotLenght + daarrt.clawBase + rotationCenter[0] , daarrt.robotWidth/2 + daarrt.clawWidthOpened * daarrt.clawOpening/180.0 + rotationCenter[1])

    #robotTmp = [pylygon.Polygon(body) , pylygon.Polygon(clawBase) , pylygon.Polygon(wheel1) , pylygon.Polygon(wheel2) , pylygon.Polygon(wheel3) , pylygon.Polygon(wheel4) , pylygon.Polygon(claw1) , pylygon.Polygon(claw2)]
    #robot = [poly_translate(poly_rotate(element,daarrt.robotCap),daarrt.posX,daarrt.posY) for element in robotTmp]

    robotTmp = [pylygon.Polygon(body) , pylygon.Polygon(frontId) , pylygon.Polygon(wheel1) , pylygon.Polygon(wheel2) , pylygon.Polygon(wheel3) , pylygon.Polygon(wheel4)]
    robot = [poly_translate(poly_rotate(element,daarrt.robotCap),daarrt.posX,daarrt.posY) for element in robotTmp]

    return robot

def createObstacle(world,x,y):

    '''
    return :
        pylygon object corresponding to an obstacle

    arguments :
        x : position on x Axis
        y : position on y Axis

    '''

    obs=pylygon.Polygon([(x,y),(x+world.elementSize,y),(x+world.elementSize,y+world.elementSize),(x,y+world.elementSize)])

    return obs

def createWall(world,num_case,num_line):

    '''
    return :
        list of pylygon object corresponding to the walls of a World

    arguments :
        num_case : number of case
        num_line : number of line

    '''

    polyObs1=[(0,0),((num_case) * world.elementSize,0),((num_case) * world.elementSize,world.elementSize),(0,world.elementSize)]
    polyObs2=[(0,world.elementSize),(world.elementSize,world.elementSize),(world.elementSize,(num_line) * world.elementSize),(0,(num_line) * world.elementSize)]
    polyObs3=[((num_case - 1) * world.elementSize,world.elementSize),((num_case) * world.elementSize,world.elementSize),((num_case) * world.elementSize,(num_line - 1) * world.elementSize),(((num_case - 1) * world.elementSize,(num_line - 1) * world.elementSize))]
    polyObs4=[(0,(num_line - 1) * world.elementSize),(num_case * world.elementSize,(num_line - 1) * world.elementSize),(num_case*world.elementSize,num_line * world.elementSize),(0,num_line * world.elementSize)]
    polyObs5=[(18*world.elementSize,0),(19*world.elementSize,0),(19*world.elementSize,12*world.elementSize), (18*world.elementSize,12*world.elementSize)]
    polyObs6=[(31*world.elementSize,11*world.elementSize),(32*world.elementSize,11*world.elementSize), (32*world.elementSize,(num_line-1)*world.elementSize), (31*world.elementSize,(num_line-1)*world.elementSize)]
              
    walls=[pylygon.Polygon(polyObs1),pylygon.Polygon(polyObs2),pylygon.Polygon(polyObs3),pylygon.Polygon(polyObs4)]
    walls=[pylygon.Polygon(polyObs1),pylygon.Polygon(polyObs2),pylygon.Polygon(polyObs3),pylygon.Polygon(polyObs4),pylygon.Polygon(polyObs5),pylygon.Polygon(polyObs6)]

    return walls

def poly_translate (p, tx, ty):

    '''
    return :
        pylygon object corresponding to the argument translated

    arguments :
        p  : pylygon object to translate
        tx : translation on X axis
        ty : translation on Y axis

    '''

    points = p.P
    pointsTranslates = array([(x+tx,y+ty) for (x,y) in points])
    p.P = pointsTranslates

    return pylygon.Polygon(p)

def poly_rotate (p, theta):

    '''
    return :
        pylygon object corresponding to the argument rotated

    arguments :
        p  : pylygon object to rotate
        theta : rotation angle in degrees

    '''

    theta=theta * math.pi/180.0
    points=p.P
    pointsTournes = array([(x * math.cos(theta)-y * math.sin(theta),
                  x * math.sin(theta) + y * math.cos(theta)) for (x,y) in points])
    p.P=pointsTournes

    return pylygon.Polygon(p)
