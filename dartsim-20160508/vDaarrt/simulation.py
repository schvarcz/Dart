'''
@auhtor : Corentin R
@date : February 2015

This file contains the function called by the programm when running on simulation

'''


import pygame,pylygon,threading,sys,time
from pygame.locals import *

from modules.daarrt2d import *
from modules.world import *
from modules.constantes import *
from modules.info import *

HIGH    = "1"
LOW     = "0"
INPUT   = "0"
OUTPUT  = "1"


def simulate(ns,package,changeData,changeDataEnco,sonarLeft,sonarRight, sonarFront , sonarBack , changeCap):

    #creation of objects required
    myWorld=World(worldName)
    worldLenght=myWorld.generer()
    pygame.init()
    simu=pygame.display.set_mode((worldLenght[0]+windowWidth,worldLenght[1]))
    info=Info(worldLenght)
    bg=pygame.image.load(background).convert()
    pygame.display.set_caption(titre)

    #first printingFront
    pos=myWorld.afficher(simu,True)
    daarrt2d=DAARRT2d(pos)


    #simulation loop
    pygame.key.set_repeat(400, 30)
    runSimu=True
    display=0

    while(runSimu==True) :
        #Limitation vitesse
        pygame.time.Clock().tick(speed)
        simu.blit(bg,(0,0))
        myWorld.afficher(simu,False)

        package,changeData=cleanBus(package,changeData,changeDataEnco,daarrt2d)
        runSimu=daarrt2d.update(package,myWorld,changeCap)
        info.afficher(simu,daarrt2d,display)
        daarrt2d.draw(simu)
        virtualSonar(daarrt2d,myWorld,sonarLeft,sonarRight,sonarFront,sonarBack)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                runSimu = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0]<worldLenght[0] + 40 and event.pos[0] > worldLenght[0] + 10 and event.pos[1] < worldLenght[1] - 30 and event.pos[1] > worldLenght[1] - 60 :
                display += 1
                if display >= 2 :
                    display = 0
            if event.type == KEYDOWN and event.key == K_l :

                if display == 2 :

                    display = 0

                else :

                    display = 2
        runSimu = ns.isAlive

    print "Ending Simulation..."
    pygame.quit()
    #ns.isAlive=False

def cleanBus(package,changeData,changeDataEnco,daarrt):
    '''
    return the package updated and the element change Data cleaned

    args :
        package : dictionnary corresponding to the bus
        changeData : list of elements which changed since the last update
    '''

    while(len(changeData)>0):
        try :
            package[changeData[-1][0]]=changeData[-1][1]
            changeData.pop()
        except : pass
    while(len(changeDataEnco)>0):
        try :
            changeDataEnco.pop()
        except : pass
    changeDataEnco.append(["LeftEnco",daarrt.leftEnco])
    changeDataEnco.append(["RightEnco",daarrt.rightEnco])
    return package,changeData

def virtualSonar(daarrt2d,world,sonarLeft,sonarRight,sonarFront,sonarBack):
    changeSonarLeft = sonarLeft.changeSonarLeft
    changeSonarRight = sonarRight.changeSonarRight
    changeSonarFront = sonarFront.changeSonarFront
    changeSonarBack = sonarBack.changeSonarBack
    
    try :
        if(len(changeSonarLeft)>1):
            changeSonarLeft.pop()
    except :  print "FailLeft"

    changeSonarLeft.append(daarrt2d.sonarDist[2])

    try :
        if(len(changeSonarRight)>1):

            changeSonarRight.pop()

    except : print "FailRight"

    changeSonarRight.append(daarrt2d.sonarDist[3])

    try :
        if(len(changeSonarFront)>1) :
            changeSonarFront.pop()


    except : print "FailFront"
    changeSonarFront.append(daarrt2d.sonarDist[0])
    #print changeSonarFront
    
    try :
        if(len (changeSonarBack)>1):
            changeSonarBack.pop()

    except : print "FailBack"
    changeSonarBack.append(daarrt2d.sonarDist[1])


dtSonar = 0.0000001
dtChange = 0.001
        

def sonarFrontDeamon(ns,sonarFront,changeSonarFront):
    print "Starting Front Sonar Deamon..."
    simuOn=True
    tMax=5.0*2.0/3.4 # 5 meters max
    tFront=tMax
    propag=False
    tx = sonarFront.tx
    rx = sonarFront.rx
    t0=time.time()
    while simuOn:
        if ((time.time()-t0) > dtChange) and (not(propag)):
            t0=time.time()
            try:
                if len(changeSonarFront)>1:
                    val=changeSonarFront.pop()
                    tFront=2.0*val/34000.0
                    #print len(changeSonarFront),val
                    changeSonarFront.append(val)
                    #print len(changeSonarFront)
            except:
                # can't get sonar
                #tFront = tMax
                pass
        if tx.read() == HIGH:
            rx.write(HIGH)
            print "tx Front"
            t0=time.time()
            propag=True
        if propag:
            if(time.time()-t0) > tFront:
                rx.write(LOW)              
                #print "rx front",val,(time.time()-t0)*34000.0/2.0
                propag=False
        # time.sleep(0.00001) # pulse used in real sonar
        time.sleep(dtSonar)
        simuOn = ns.isAlive
    print "Ending Front Sonar Deamon..."


def sonarBackDeamon(ns,sonarBack,changeSonarBack):
    print "Starting Back Sonar Deamon..."
    simuOn=True
    tMax=5.0*2.0/3.4 # 5 meters max
    tBack=tMax
    propag=False
    tx = sonarBack.tx
    rx = sonarBack.rx
    t0=time.time()
    while simuOn:
        if ((time.time()-t0) > dtChange) and (not(propag)):
            t0=time.time()
            try:
                if len(changeSonarBack)>1:
                    val=changeSonarBack.pop()
                    tBack=2.0*val/34000.0
                    #print len(changeSonarBack),val
                    changeSonarBack.append(val)
                    #print len(changeSonarBack)
            except:
                # can't get sonar
                #tBack = tMax
                pass
        if tx.read() == HIGH:
            rx.write(HIGH)
            print "tx Back"
            t0=time.time()
            propag=True
        if propag:
            if(time.time()-t0) > tBack:
                rx.write(LOW)              
                #print "rx Back",val,(time.time()-t0)*34000.0/2.0
                propag=False
        # time.sleep(0.00001) # pulse used in real sonar
        time.sleep(dtSonar)
        simuOn = ns.isAlive
    print "Ending Back Sonar Deamon..."


def sonarLeftDeamon(ns,sonarLeft,changeSonarLeft):
    print "Starting Left Sonar Deamon..."
    simuOn=True
    tMax=5.0*2.0/3.4 # 5 meters max
    tLeft=tMax
    propag=False
    tx = sonarLeft.tx
    rx = sonarLeft.rx
    t0=time.time()
    while simuOn:
        if ((time.time()-t0) > dtChange) and (not(propag)):
            t0=time.time()
            try:
                if len(changeSonarLeft)>1:
                    val=changeSonarLeft.pop()
                    tLeft=2.0*val/34000.0
                    #print len(changeSonarLeft),val
                    changeSonarLeft.append(val)
                    #print len(changeSonarLeft)
            except:
                # can't get sonar
                #tLeft = tMax
                pass
        if tx.read() == HIGH:
            rx.write(HIGH)
            print "tx Left"
            t0=time.time()
            propag=True
        if propag:
            if(time.time()-t0) > tLeft:
                rx.write(LOW)              
                #print "rx Left",val,(time.time()-t0)*34000.0/2.0
                propag=False
        # time.sleep(0.00001) # pulse used in real sonar
        time.sleep(dtSonar)
        simuOn = ns.isAlive
    print "Ending Left Sonar Deamon..."


def sonarRightDeamon(ns,sonarRight,changeSonarRight):
    print "Starting Right Sonar Deamon..."
    simuOn=True
    tMax=5.0*2.0/3.4 # 5 meters max
    tRight=tMax
    propag=False
    tx = sonarRight.tx
    rx = sonarRight.rx
    t0=time.time()
    while simuOn:
        if ((time.time()-t0) > dtChange) and (not(propag)):
            t0=time.time()
            try:
                if len(changeSonarRight)>1:
                    val=changeSonarRight.pop()
                    tRight=2.0*val/34000.0
                    #print len(changeSonarRight),val
                    changeSonarRight.append(val)
                    #print len(changeSonarRight)
            except:
                # can't get sonar
                #tRight = tMax
                pass
        if tx.read() == HIGH:
            rx.write(HIGH)
            print "tx Right"
            t0=time.time()
            propag=True
        if propag:
            if(time.time()-t0) > tRight:
                rx.write(LOW)              
                #print "rx Right",val,(time.time()-t0)*34000.0/2.0
                propag=False
        # time.sleep(0.00001) # pulse used in real sonar
        time.sleep(dtSonar)
        simuOn = ns.isAlive
    print "Ending Right Sonar Deamon..."
