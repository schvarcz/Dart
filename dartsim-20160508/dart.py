#!/usr/bin/python
# -*- coding: utf-8 -*-

# Second Year ENSTA Bretagne SPID Project
#    D : Brian Detourbet
#    A : Elouan Autret
#    A : Fahad Al Shaik
#    R : Corentin Rifflart
#    R : Clémenet Rodde
#    T : Rémi Terrien

# Code modified in May 2016, by BenBlop

import os
import time
import math
import struct
# import sys

def high_low_int(high_byte, low_byte):
    '''
    Convert low and low and high byte to int
    '''
    return (high_byte << 8) + low_byte

def high_byte(integer):
    '''
    Get the high byte from a int
    '''
    return integer >> 8


def low_byte(integer):
    '''
    Get the low byte from a int
    '''
    return integer & 0xFF

class Daarrt():
    def __init__(self):

        self.motor_last_change = 0

        if os.access("/var/www/daarrt.conf", os.F_OK) :
            print "Real DAARRT creation"

            # Import modules
            from drivers.trex import TrexIO
            from drivers.razor import RazorIO
            #from drivers.hcsr04 import SonarIO
            from drivers.sonar import SonarIO
            self.trex = TrexIO(0x07)
            self.razor = RazorIO()
            #self.sonar = [SonarIO(2, 3), SonarIO(4, 5), SonarIO(6, 7), SonarIO(8, 9)] # [Arriere, Droite, Avant, Gauche]
            self.sonarLeft = SonarIO("back")
            self.sonarRight = SonarIO("right")
            self.sonarFront = SonarIO("front")
            self.sonarBack =  SonarIO("left")
            self.sonar = [self.sonarBack,self.sonarRight,self.sonarFront,self.sonarLeft] # [Arriere, Droite, Avant, Gauche]

        else :
            print "Create virtual DAARRT"

            from multiprocessing import Process,Manager
            import vDaarrt.simulation as simulation
            import vDaarrt.modules.vTrex as vTrex
            import vDaarrt.modules.vSonar as vSonar
            import vDaarrt.modules.vRazor as vRazor

            global simuProc,sonarDmn

            manager = Manager()
            self.ns = manager.Namespace()
            self.trex = vTrex.vTrex()
            self.razor = vRazor.vRazorIO()
            self.sonarLeft = vSonar.vSonar("left")
            #print self.sonarLeft.__dict__
            self.sonarRight = vSonar.vSonar("right")
            self.sonarFront = vSonar.vSonar ("front")
            self.sonarBack = vSonar.vSonar("back")
            self.sonar = [self.sonarBack,self.sonarRight,self.sonarFront,self.sonarLeft]
            self.ns.isAlive = True
            simuProc = Process(target = simulation.simulate,args = (self.ns,self.trex.package,self.trex.changeData,self.trex.changeDataEnco,self.sonarLeft,self.sonarRight,self.sonarFront,self.sonarBack,self.razor.changeCap))
            simuProc.start()
            print "Running Simulation"
            sonarFrontDaemon = Process(target = simulation.sonarFrontDeamon, args=(self.ns, self.sonarFront,self.sonarFront.changeSonarFront))
            sonarBackDaemon = Process(target = simulation.sonarBackDeamon, args=(self.ns, self.sonarBack,self.sonarBack.changeSonarBack))
            sonarLeftDaemon = Process(target = simulation.sonarLeftDeamon, args=(self.ns, self.sonarLeft,self.sonarLeft.changeSonarLeft))
            sonarRightDaemon = Process(target = simulation.sonarRightDeamon, args=(self.ns, self.sonarRight,self.sonarRight.changeSonarRight))
            #self.sonarRight,self.sonarRight.changeSonarRight,self.sonarLeft,self.sonarLeft.changeSonarLeft))
            sonarFrontDaemon.start()
            sonarBackDaemon.start()
            sonarLeftDaemon.start()
            sonarRightDaemon.start()
            print "Running Sonar Deamons"


    ###########################
    ##          T-REX        ##
    ###########################

    def status(self):
        '''
        Read status from trex
        Return as a byte array
        '''
        raw_status = self.trex.i2cRead()
        return struct.unpack(">cchhHhHhhhhhh", raw_status)[2:]


    def reset(self):
        '''
        Reset the trex controller to default
        Stop dc motors...
        '''
        self.trex.reset()


    def motor(self, left, right):
        '''
        Set speed of the dc motors
        left and right can have the folowing values: -255 to 255
        -255 = Full speed astern
        0 = stop
        255 = Full speed ahead
        '''
        self.motor_last_change = time.time()*1000

        # put your code here

        # set left motor speed
        self.trex.package['lm_speed_high_byte'] = 0
        self.trex.package['lm_speed_low_byte'] = 0
        # set right motor speed
        self.trex.package['rm_speed_high_byte'] = 0
        self.trex.package['rm_speed_low_byte'] = 0
        # write the 27 bytes in package on the i2C bus
        self.trex.i2cWrite()  


    def servo(self, servo, position):
        '''
        Set servo position
        Servo = 1 to 6
        Position = Typically the servo position should be a value between 1000 and 2000 although it will vary depending on the servos used
        '''
        servo = str(servo)
        position = int(position)
        self.trex.package['servo_' + servo + '_high_byte'] = high_byte(position)
        self.trex.package['servo_' + servo + '_low_byte'] = low_byte(position)
        self.trex.i2cWrite()

    def encoder(self):
        leftEnco = 0
        rightEnco = 0
        # put your code here

        return leftEnco,rightEnco
        

    ###########################
    ##    Razor 9-DOF IMU    ##
    ###########################

    def getAngles(self):
        '''
        Return angles measured by the Razor (yaw/pitch/roll calculated automatically from the 9-axis data).
        '''
        return struct.unpack('fff', self.razor.getAngles())

    def getSensorData(self):
        """
            Output SENSOR data of all 9 axes in text format.
            One frame consist of three 3x3 float values = 36 bytes. Order is: acc x/y/z, mag x/y/z, gyr x/y/z.
        """
        return struct.unpack('fffffffff', self.razor.getRawSensorData())

    def getCalibratedSensorData(self):
        """
            Output CALIBRATED SENSOR data of all 9 axes in text format.
            One frame consist of three 3x3 float values = 36 bytes. Order is: acc x/y/z, mag x/y/z, gyr x/y/z.
        """
        return struct.unpack('fffffffff', self.razor.getCalibratedSensorData())

    ###########################
    ##     Sonar HC-SR04     ##
    ###########################

    def getSonars(self):
        '''
        Return angles measured by the Razor (calculated automatically from the 9-axis data).
        '''
        dist = [s.dist() for s in self.sonar]
        #for name, val in zip(["Sonar " + i + " : " for i in ["arriere", "droite", "avant", "gauche"]], dist) :
        #    if val == -1 : print name + "range <= 5 cm"
        #    else : print name + "%.1f" % val
        return dist

if __name__ == "__main__":
    # insert your test code here , example :
    myDart = Daarrt()
    
    # test motor commands
    myDart.motor(50,50)
    # time.sleep(20)

    # myDart.motor(-50,50)
    # time.sleep(2)

    # myDart.motor(50,50)
    # time.sleep(2)
 
    # myDart.motor(-50,-50)
    # time.sleep(2)
  
    while myDart.ns.isAlive:
        time.sleep(2)
    # end of simulation
    myDart.ns.isAlive=False
    
    # wait 1s to cleanly the end of simulation
    time.sleep(1) 