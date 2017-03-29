import struct
from multiprocessing import Process,Manager


class vRazorIO():
    def __init__(self):
        manager=Manager()
        self.changeCap=manager.list()
        self.changeCap.append(0.0)

    def getAngles(self):

        try :
            head0 = self.changeCap[-1]
            head = (head0+90.0+360.0)%360.0
            #print head0,head
            output=struct.pack("fff",head,0.0,0.0)

        except:
            print "Can't get value"
            output=struct.pack("fff",0.0,0.0,0.0)
        return output

    def getRawSensorData(self):
        output=struct.pack("fffffffff",0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
        return output

    def getCalibratedSensorData(self):
        output=struct.pack("fffffffff",0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
        return output
