#!/usr/bin/python
# -*- coding: utf8 -*-

#import ConfigParser
import serial
import struct
import os
import time

VALID_STATES = ["#o0", "#o1", "#ob", "#ot", "#oc", "#on", "#osct", "#osrt", "#osbt", "#oscb", "#osrb", "#osbb", "#oe0", "#oe1", "#f", "#s<xy>"]

class RazorIO():
    def __init__(self):

        # Setting GPIO 0 & 1 in UART mode
        #os.system("sudo modprobe gpio")  # seems to be ok at boot
        os.system('echo "3" > /sys/devices/virtual/misc/gpio/mode/gpio0')
        os.system('echo "3" > /sys/devices/virtual/misc/gpio/mode/gpio1')

        # Opening the serial communication bus (baudrate = 9600)
        self.bus = serial.Serial('/dev/ttyS1', 57600, timeout = 10)
        self.state = "#ob"
        self.bus.write(self.state) # Setting default state to binary angle output

    def __setState(self, state):
        if state in VALID_STATES :
            self.bus.write(state)
            self.bus.flush()
            self.state = state
        else :
            print "Commande invalide !"

    def getAngles(self):

        """
            Output angles in BINARY format (yaw/pitch/roll as binary float, so one output frame
            is 3x4 = 12 bytes long)
        """

        if self.state != '#ob': self.__setState('#ob')
        self.bus.write("#f")
        self.bus.flush()
        output = self.bus.read(12)
        self.__update(output)

        return output

    def getRawSensorData(self):

        """
            Output RAW SENSOR data of all 9 axes in BINARY format.
            One frame consist of three 3x3 float values = 36 bytes. Order is: acc x/y/z, mag x/y/z, gyr x/y/z.
        """

        if self.state != '#osrb': self.__setState('#osrb')
        self.bus.write("#f")
        output = self.bus.read(36)
        self.__update(output)

        return output

    def getCalibratedSensorData(self):

        """
            Output CALIBRATED SENSOR data of all 9 axes in BINARY format.
            One frame consist of three 3x3 float values = 36 bytes. Order is: acc x/y/z, mag x/y/z, gyr x/y/z.
        """

        if self.state != '#oscb': self.__setState('#oscb')
        self.bus.write("#f")
        output = self.bus.read(36)
        self.__update(output)

        return output

    def __update(self, raw_data):
        pass
#
#        conf = ConfigParser.ConfigParser()
#        conf.read("/var/www/daarrt.conf")
#        if not conf.has_section("razor") : conf.add_section("razor")
#
#        data = struct.unpack("f"*(len(raw_data)/4), raw_data)
#
#        # Update angles
#        if self.state == '#ob' : data = zip(['Yaw', 'Pitch', 'Roll'], data)
#        elif self.state == '#osrb' :
#            data = zip(['Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z',
#                        'Magnetometer_X', 'Magnetometer_Y', 'Magnetometer_Z',
#                        'Gyroscope_X', 'Gyroscope_Y', 'Gyroscope_Z'], data)
#        elif self.state == '#oscb' :
#            data = zip(['Calibrated_accelerometer_X', 'Calibrated_accelerometer_Y', 'Calibrated_accelerometer_Z',
#                        'Calibrated_magnetometer_X', 'Calibrated_magnetometer_Y', 'Calibrated_magnetometer_Z',
#                        'Calibrated_gyroscope_X', 'Calibrated_gyroscope_Y', 'Calibrated_gyroscope_Z'], data)
#
#        for i, j in data : conf.set("razor", i, j)
#
#        fd = open("/var/www/daarrt.conf", 'w')
#        conf.write(fd)
#        fd.close()
    def getData(self):
        if self.state != '#ob': self.__setState('#ob')
        if self.state != '#o0': self.__setState('#o0')
        self.bus.write("#f")
        self.bus.flush()
        rzrdata = struct.unpack("fff",self.bus.read(12))
        nc = len(rzrdata)
        return nc,rzrdata

    def getDataOld(self):
        self.bus.write("#osrt")  # raw
        #self.cmd.write("#osct")  # calib
        #self.cmd.write("#osbt")  # both
        self.bus.write("#f")
        self.bus.flush()
        nc,razdata=self.getSerial(1.0)
        #print razdata
        return nc,razdata
        
    def getSerial(self,timeOut):
        st=""
        cnt=0
        nc=0
        while True:
            nc = self.bus.inWaiting()
            #print nc
            if nc != 0:
                st = self.bus.read(nc)
                break
            time.sleep(timeOut/10.0)
            cnt += 1
            if (cnt == 10):
                break
        return nc,st


if __name__ == "__main__":
    
    rz = RazorIO();

    for k in range(5):
        print rz.getData()
	time.sleep(0.2)