# -*- coding: utf-8 -*-
"""
Created on Fri May  6 16:52:13 2016

@author: the daarrt team and benblop 
"""

import os
import time
#import ConfigParser

## For simplicity's sake, we'll create a string for our paths.
GPIO_MODE_PATH = os.path.normpath('/sys/devices/virtual/misc/gpio/mode/')
GPIO_PIN_PATH  = os.path.normpath('/sys/devices/virtual/misc/gpio/pin/')
GPIO_FILENAME  = "gpio"

## Create a few strings for file I/O equivalence
HIGH    = "1"
LOW     = "0"
INPUT   = "0"
OUTPUT  = "1"

class GPIO():
    def __init__(self, i) :
        self.__mode = os.path.join(GPIO_MODE_PATH, 'gpio'+str(i))
        self.__data = os.path.join(GPIO_PIN_PATH, 'gpio'+str(i))
	#print self.__mode
        self.clean()

    def set(self, state) :
        with open(self.__mode, 'w+') as f:
            f.write(state)

    def read(self) :
        with open(self.__data, 'r') as f:
            return f.read(1)

    def write(self, state) :
        with open(self.__data, 'w') as f:
            f.write(state)

    def clean(self) :
        self.set(OUTPUT)
        self.write(LOW)


SONAR_NAMES = ["back", "right", "front", "left"]
PIN_MAP = {"back":(2,3), "right":(4,5), "front":(6,7), "left":(8,9)}

class SonarIO():
    def __init__(self, name):
        self.sonar_name = name
        self.PIN_GPIO_ECHO = PIN_MAP[self.sonar_name][0]
        self.PIN_GPIO_TRIGGER = PIN_MAP[self.sonar_name][1]
        #print self.PIN_GPIO_TRIGGER

        self.GPIO_ECHO = GPIO(self.PIN_GPIO_ECHO)
        self.GPIO_TRIGGER = GPIO(self.PIN_GPIO_TRIGGER)

        self.GPIO_ECHO.set(INPUT)
        self.GPIO_TRIGGER.set(OUTPUT)

        time.sleep(0.5)

    def dist(self):
        # Send 20us pulse to trigger
        self.GPIO_TRIGGER.write(HIGH)
        time.sleep(0.00002)
        self.GPIO_TRIGGER.write(LOW)

        # Sometimes the answer is too fast so it isn't caught, 
        # sometimes the 10us pulse is not caught by the PCDuino 
        #    (python not much precise with time.sleep())
        start = time.time()
        iteration = 0
        #print self.GPIO_ECHO.read()
        while self.GPIO_ECHO.read() == LOW:
            if (time.time() - start) > 0.029 :
                if (iteration > 5) :
                    break
            iteration += 1 
        start = time.time()

        stop = start
        while self.GPIO_ECHO.read() == HIGH :
           stop = time.time()
           if (stop - start > .029) : break

        try :
           # Calculate pulse length
           elapsed = stop-start

           # Distance pulse travelled in that time is time
           # multiplied by the speed of sound (cm/s)
           distance = elapsed * 34000

           # That was the distance there and back so halve the value
           distance = distance / 2

           #print "Distance : %.1f" % distance

        except UnboundLocalError :
           #print ("<= 5")
           distance = -1.0
        return distance

if __name__ == "__main__":
    tSonar=[] 
    tDist=[]
    for name in SONAR_NAMES:
	#print name
        tSonar.append(Sonar(name))
        tDist.append(0.0)

    while True:
      i=0
      for snr in tSonar:
 	tDist[i] = snr.dist()
	i+=1
      print SONAR_NAMES[0],SONAR_NAMES[1],SONAR_NAMES[2],SONAR_NAMES[3]
      print "%5d  %5d  %5d  %5d"%(tDist[0],tDist[1],tDist[2],tDist[3])
      time.sleep(1.0)


	

