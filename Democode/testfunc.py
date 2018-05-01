#!/usr/bin/python

from LIS3DH import LIS3DH
from TempHeader1 import temp_sensor
from time import sleep

tempsensor = temp_sensor()

if __name__ == '__main__':
    sensor = LIS3DH(debug=True)
    sensor.setRange(LIS3DH.RANGE_2G)
    
    

    print("Starting stream")
    while True:

        x = sensor.getX()
        y = sensor.getY()
        z = sensor.getZ()

        # raw values from accel
        print("\r\nX: %.6f\tY: %.6f\tZ: %.6f" % (x, y, z))
        
        # temp values
        temp = tempsensor.readTempF()
        print ("Temperature in Fahrenheit : %.2f F"%(temp))
        sleep(1)
    
