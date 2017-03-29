from multiprocessing import Process,Manager
import time
import os

SONAR_NAMES = ["back", "right", "front", "left"]
PIN_MAP = {"back":(2,3), "right":(4,5), "front":(6,7), "left":(8,9)}

class vSonar():

    def __init__(self, sonarName):

    
        GPIO_ECHO, GPIO_TRIGGER = PIN_MAP[sonarName]

        self.sonarName = sonarName
        self.tx = vGPIO(GPIO_TRIGGER)
        self.rx = vGPIO(GPIO_ECHO)
        self.tx.set(OUTPUT)
        self.rx.set(INPUT)
        self.tx.write(LOW)

        manager=Manager()
        if(sonarName == "left"):
            self.changeSonarLeft=manager.list()
            print "define sonar ",sonarName            
        elif (sonarName == "right"):
            self.changeSonarRight=manager.list()
            print "define sonar ",sonarName
        elif (sonarName == "front"):
            self.changeSonarFront=manager.list()
            print "define sonar ",sonarName
        elif (sonarName == "back"):
            self.changeSonarBack=manager.list()
            print "define sonar ",sonarName
        else :
            pass
        
    def dist(self):
        # Send 20us pulse to trigger
        self.tx.write(HIGH)
        time.sleep(0.00002)
        self.tx.write(LOW)

        # Sometimes the answer is too fast so it isn't caught, 
        # sometimes the 10us pulse is not caught by the PCDuino 
        #    (python not much precise with time.sleep())
        start = time.time()
        iteration = 0
        #print self.GPIO_ECHO.read()
        while self.rx.read() == LOW:
            if (time.time() - start) > 0.029 :
                if (iteration > 5) :
                    break
            iteration += 1 
        #print "epsilon time = ",time.time()-start
        start = time.time()
        
        while self.rx.read() == HIGH :
            stop = time.time()
            if (stop - start > 0.029) :
                break
        
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
        #print "distance = ",distance
        return distance


    def distOld(self) :
        try :
            if(self.sonarName=="left"):
                return self.changeSonarLeft[-1]
            elif (self.sonarName == "right"):
                return self.changeSonarRight[-1]
            elif (self.sonarName == "front"):
                return self.changeSonarFront[-1]
            elif (self.sonarName == "back"):
                return self.changeSonarBack[-1]
            else :
                pass
        except :
            return -1

HIGH    = "1"
LOW     = "0"
INPUT   = "0"
OUTPUT  = "1"

class vGPIO():
    def __init__(self, iPin) :
        self.__mode = '/sys/devices/virtual/misc/gpio/mode/gpio'+str(iPin)
        self.__data = '/sys/devices/virtual/misc/gpio/pin/gpio'+str(iPin)
#        os.system("mkdir gpio")
#        os.system("mkdir gpio/mode")
#        os.system("mkdir gpio/pin")
#        os.system("chmod -R 777 gpio") 
        self.__sim_mode = 'gpio/mode/gpio'+str(iPin)
        self.__sim_data = 'gpio/pin/gpio'+str(iPin)
        
    def set(self, state) :
        #try:
        #    with open(self.__mode, 'w+') as f:
        #        f.write(state)
        #except:
            with open(self.__sim_mode, 'w+') as f:
                f.write(state)

    def read(self) :
        #try:
        #    with open(self.__data, 'r') as f:
        #        return f.read(1)
        #except:
            with open(self.__sim_data, 'r') as f:
                return f.read(1)
                
    def write(self, state) :
        #try:
        #    with open(self.__data, 'w') as f:
        #        f.write(state)
        #except:         
            with open(self.__sim_data, 'w') as f:
                f.write(state)

    def clean(self) :
        self.set(OUTPUT)
        self.write(LOW)
