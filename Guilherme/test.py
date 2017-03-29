from dart.dart import *




if __name__ == "__main__":

    # insert your test code here , example :
    myDart = Daarrt.getRobot()
    time.sleep(2)

    # test encoders
    myDart.motor(50,50)
    for i in range(50):
        print i,myDart.getAngles()
        time.sleep(0.25)
        
    
    # put the robot to heading between 50 and 150
    myDart.motor(60,60)
    turnOn = True
    while turnOn:
        head = myDart.getAngles()[0]
        print head
        if (head > 50) and (head < 150):
            turnOn=False
        else:
            time.sleep(0.5)

    myDart.motor(0,0)

    try:
        # end of simulation
        myDart.ns.isAlive=False
    
        # wait 1s to cleanly the end of simulation
        time.sleep(1)
    except:
        pass