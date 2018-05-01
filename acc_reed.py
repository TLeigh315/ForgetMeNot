#!/usr/bin/python

from LIS3DH import LIS3DH
from TempHeader1 import temp_sensor
import time

sensor = LIS3DH()

movingcar = 1 # max aceleration in m/s^2
lastx = 0 #last known X Coordinates
lasty = 0 #last known Y Coordinates
lastz = 0 #last known Z Coordinates
differencex = 0 # difference between current and last known X Coordinates
differencey = 0 # difference between current and last known Y Coordinates
differencez = 0 # difference between current and last known Z Coordinates
update_time = 1 #check reed sensor every second
start_program = 0

print("Starting stream")



def rateAccel(float currentx, float currenty, float currentz) :
    differencex = currentx - lastx
    differencey = currenty - lasty
    differencez = currentz - lastz
    print("\rdifferenceX: %.6f\tdifferenceY: %.6f\tdifferenceZ: %.6f \t m/s^2" % (differencex, differencey, differencez))

    if (abs(differencex)>movingcar) | (abs(differencey)>movingcar) | (abs(differencez)>movingcar) :
        print("You're moving!")
        checkReed();
        start_program = 0 #reset old coordinates to prevent false alarms when process starts over

while True:
        
    x = sensor.getX()
    y = sensor.getY()
    z = sensor.getZ()

    if start_program == 0 :
        start_program = 1
        lastx = x
        lasty = y
        lastz = z
        print("\rnewlastX: %.6f\tnewlastY: %.6f\tnewlastZ: %.6f \t m/s^2" % (x, y, z))
        
    #  Display results (acceleration is measured in m/s^2)
    print("\r\nX: %.6f\tY: %.6f\tZ: %.6f \t m/s^2" % (x, y, z))
    print("\rlastX: %.6f\tlastY: %.6f\tlastZ: %.6f \t m/s^2" % (lastx, lasty, lastz))
    
      
    time.sleep(5)
        
