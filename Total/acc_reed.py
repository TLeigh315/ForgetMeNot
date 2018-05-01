#!/usr/bin/python
import RPi.GPIO as GPIO
import serial
import subprocess
from LIS3DH import LIS3DH
import TempHeader1
import time

accelerometer = LIS3DH()
#############################################################################
movingcar = .1 # max aceleration in m/s^2
lastx = 0 #last known X Coordinates
lasty = 0 #last known Y Coordinates
lastz = 0 #last known Z Coordinates
differencex = 0 # difference between current and last known X Coordinates
differencey = 0 # difference between current and last known Y Coordinates
differencez = 0 # difference between current and last known Z Coordinates
update_time = 1 #check reed sensor every second
start_program = 0
reed_pin = 36
############################################################################

#############################################################################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(reed_pin, GPIO.IN, GPIO.PUD_DOWN)
#############################################################################

def MovingcheckReed() :
    if(GPIO.input(reed_pin) == 1) :
        print("Seat is buckled\n")

    else:
        print("Seat is unbuckled\n")
        #ReedAlertSMS()

        while True :
            print("Still not buckled")
            time.sleep(1)
            if GPIO.input(reed_pin) == 1 :
                break
       

def rateAccel(currentx, currenty, currentz) :
    differencex = currentx - lastx
    differencey = currenty - lasty
    differencez = currentz - lastz
    print("\rdifferenceX: %.6f\tdifferenceY: %.6f\tdifferenceZ: %.6f \t m/s^2" % (differencex, differencey, differencez))

    if (abs(differencex)>movingcar) | (abs(differencey)>movingcar) | (abs(differencez)>movingcar) :
        print("You're moving!")
        MovingcheckReed();
        return 1

    else :
        return 0
    
while True:
        
    x = accelerometer.getX()
    y = accelerometer.getY()
    z = accelerometer.getZ()

    if start_program == 0 : #prevents false acceleration alerts
        start_program = 1
        lastx = x
        lasty = y
        lastz = z
        print("\rnewlastX: %.6f\tnewlastY: %.6f\tnewlastZ: %.6f \t m/s^2" % (x, y, z))
        
    #  Display results (acceleration is measured in m/s^2)
    print("\r\nX: %.6f\tY: %.6f\tZ: %.6f \t m/s^2" % (x, y, z))
    print("\rlastX: %.6f\tlastY: %.6f\tlastZ: %.6f \t m/s^2" % (lastx, lasty, lastz))

    if rateAccel( x , y , z ) == 1 :
        MovingcheckReed()
        start_program = 0 #reset program

    #Update coordinate values
    lastx = x
    lasty = y
    lastz = z
    
      
    time.sleep(1)
        
