from multiprocessing import Process,Manager
import struct

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


class vTrex():

    def __init__(self):
        manager=Manager()
        self.package=manager.dict()
        self.changeData=manager.list()
        self.changeDataEnco=manager.list()
        self.initPackage()
        self.leftEnco=0
        self.rightEnco=0

    def i2cWrite(self):


        '''while len(self.changeData)>2 :
            try :
                self.changeData.pop()
            except : pass'''

        for key in self.package :
            if self.package[key] != self.oldPackage[key]:
                self.oldPackage[key]=self.package[key]
                self.changeData.append([key,self.oldPackage[key]])

    def i2cRead(self):
        try :
            self.leftEnco = int(self.changeDataEnco[0][1])
            self.rightEnco = int(self.changeDataEnco[1][1])
        except :
            pass
        print high_byte(self.leftEnco)*256 + low_byte(self.leftEnco)
        return struct.pack(">BBhhHhHhhhhhh",self.package['start_byte']
                                           ,0
                                           ,self.package['battery_high_byte']*256 + self.package['battery_low_byte']
                                           ,self.package['lm_speed_high_byte']*256 + self.package['lm_speed_low_byte']
                                           ,int(high_byte(self.leftEnco)*256 + low_byte(self.leftEnco))
                                           ,self.package['rm_speed_high_byte']*256 + self.package['rm_speed_low_byte']
                                           ,int(high_byte(self.rightEnco)*256 + low_byte(self.rightEnco))
                                           ,0
                                           ,0
                                           ,0
                                           ,0
                                           ,0
                                           ,0)


    def initPackage(self):
        self.package = {
        	'start_byte' : 15,                     # Start byte
        	'pwm_freq' : 6,                        # PWMfreq
        	'lm_speed_high_byte' : 0,              # Left speed high byte
        	'lm_speed_low_byte' : 0,               # Left Speed low byte
        	'lm_brake' : 0,                        # Left brake
        	'rm_speed_high_byte' : 0,                     # Right Speed high byte
        	'rm_speed_low_byte' : 0,               # Right Speed low byte
        	'rm_brake' : 0,                        # Right brake
        	'servo_1_high_byte' : 0,               # Servo 1 high byte
        	'servo_1_low_byte' : 0,                # Servo 1 low byte
        	'servo_2_high_byte' : 0,               # Servo 2 high byte
        	'servo_2_low_byte' : 0,                # Servo 2 low byte
        	'servo_3_high_byte' : 0,               # Servo 3 high byte
        	'servo_3_low_byte' : 0,                # Servo 3 low byte
        	'servo_4_high_byte' : 0,               # Servo 4 high byte
        	'servo_4_low_byte' : 0,                # Servo 4 low byte
        	'servo_5_high_byte' : 0,               # Servo 5 high byte
        	'servo_5_low_byte' : 0,                # Servo 5 low byte
        	'servo_6_high_byte' : 0,               # Servo 6 high byte
        	'servo_6_low_byte' : 0,                # Servo 6 low byte
        	'devibrate' : 50,                      # Devibrate
        	'impact_sensitivity_high_byte' : 0,    # Impact sensitivity high byte
        	'impact_sensitivity_low_byte' : 50,    # Impact sensitivity low byte
        	'battery_high_byte' : 0,               # Battery voltage high byte
        	'battery_low_byte' : 50,               # Battery voltage low byte
        	'i2c_address' : 7,                     # I2C slave address
        	'i2c_clock' : 0                       # I2C clock frequency
        }
        self.oldPackage= {
        	'start_byte' : 15,                     # Start byte
        	'pwm_freq' : 6,                        # PWMfreq
        	'lm_speed_high_byte' : 0,              # Left speed high byte
        	'lm_speed_low_byte' : 0,               # Left Speed low byte
        	'lm_brake' : 0,                        # Left brake
        	'rm_speed_high_byte' : 0,                     # Right Speed high byte
        	'rm_speed_low_byte' : 0,               # Right Speed low byte
        	'rm_brake' : 0,                        # Right brake
        	'servo_1_high_byte' : 0,               # Servo 1 high byte
        	'servo_1_low_byte' : 0,                # Servo 1 low byte
        	'servo_2_high_byte' : 0,               # Servo 2 high byte
        	'servo_2_low_byte' : 0,                # Servo 2 low byte
        	'servo_3_high_byte' : 0,               # Servo 3 high byte
        	'servo_3_low_byte' : 0,                # Servo 3 low byte
        	'servo_4_high_byte' : 0,               # Servo 4 high byte
        	'servo_4_low_byte' : 0,                # Servo 4 low byte
        	'servo_5_high_byte' : 0,               # Servo 5 high byte
        	'servo_5_low_byte' : 0,                # Servo 5 low byte
        	'servo_6_high_byte' : 0,               # Servo 6 high byte
        	'servo_6_low_byte' : 0,                # Servo 6 low byte
        	'devibrate' : 50,                      # Devibrate
        	'impact_sensitivity_high_byte' : 0,    # Impact sensitivity high byte
        	'impact_sensitivity_low_byte' : 50,    # Impact sensitivity low byte
        	'battery_high_byte' : 0,               # Battery voltage high byte
        	'battery_low_byte' : 50,               # Battery voltage low byte
        	'i2c_address' : 7,                     # I2C slave address
        	'i2c_clock' : 0                       # I2C clock frequency
        }
