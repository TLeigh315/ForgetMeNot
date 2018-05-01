#!/usr/bin/python
import RPi.GPIO as GPIO
import serial
import subprocess
from LIS3DH import LIS3DH
import TempHeader1
import time

#############################################################################
accelerometer = LIS3DH()
accel_sensor = TempHeader1.accelerometer_sensor()
alert = TempHeader1.alert()
#############################################################################

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
timer = 0 #initiate timer
timer_speed = 1
last_alert = 0
reed_bit = 0 # seat belt check. 1 = unbuckled, 0 = buckled
############################################################################

############################################################################
dev = subprocess.check_output('ls /dev/ttyACM*', shell=True) #find out what name the Arduino is under
print (dev) #display Arduino name (will be shown in bytes)
dev=dev.decode("utf-8") #convert Arduino name from bytes to string
dev=dev.replace("\n","") #get rid of \n

try:
    ser = serial.Serial(dev,9600) # Connect to Arduino's Serial
    print ("Connected to Arduino")
except:
    print ("Arduino not connected")
############################################################################

#############################################################################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(reed_pin, GPIO.IN, GPIO.PUD_DOWN)
#############################################################################

while True:
    print("\r\nCurrent time is: " +str(timer))
    print("Last alert time: " + str(last_alert))
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
    print("\rX: %.6f\tY: %.6f\tZ: %.6f \td m/s^2" % (x, y, z))
    print("\rlastX: %.6f\tlastY: %.6f\tlastZ: %.6f \t m/s^2" % (lastx, lasty, lastz))

    if accel_sensor.rateAccel(movingcar, x, y, z, lastx, lasty, lastz) == 1 :
        belt_check = accel_sensor.MovingcheckReed(GPIO.input(reed_pin), last_alert, timer)#check if kid is buckled while the car is moving

        last_alert = belt_check['last_alert'] #update last alert time

        if belt_check['reed_bit'] == 1 :
            alert.seat_belt_alert(ser)    
                
        start_program = 0 #reset program values

    #Update coordinate values
    lastx = x
    lasty = y
    lastz = z
    
    time.sleep(1)
    timer = timer + 1
    
