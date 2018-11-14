#!/usr/bin/python

import thread
import RPi.GPIO as GPIO
import subprocess
import GSMheader
import AccelSensorHeader
import LIS3DH
import TempHeader1
import time
import bluetooth
import smbus
import serial
import pygame
from subprocess import call
from threading import Thread
from Queue import Queue
import threading
import random
import sys
import numpy as np
import cv2
from pylepton import Lepton
from time import sleep


#CREATE OBJECTS FROM HEADER CLASSES##########################################
accelerometer = LIS3DH.LIS3DH() #Create LIS3DH accelerometer
accel_sensor = AccelSensorHeader.accelerometer_sensor() #Create object for accelerometer_sensor class
tempsensor = TempHeader1.temp_sensor()#Create MCP9808 temp sensor object
#############################################################################

# INITIAL ACCELEROMETER DATA###################################################
movingcar = .1 # max aceleration in m/s^2
lastx = 0 #last known X Coordinates
lasty = 0 #last known Y Coordinates
lastz = 0 #last known Z Coordinates
last_caralert = 0
############################################################################

###########################################################################################
danger_rate = 1.9
maxtemp = 89 #maximum temperature
temp_rate = 0 #difference between current and last temperature
base_temp = 0
start_time = 0 #TEMPORARY
last_alert = 0 #time since last alert
base_time = 0
tempstart = 0
first_alert= 0 #time of first alert
child_danger_rate = 1.9
child_maxtemp = 200
child_base_temp = 0
child_base_time = 0
camera_start = 0
camera_last_alert = 0
camera_first_alert = 0
#########################################################################################

############################################################################
EMSnum = "8327978415"
phonenum = "8304809421"
backupnum = "\r"
car_color = "\r"
car_type = "\r"
License_plate = "\r"
Longitude = "\r"
Latitude = "\r"
connection_bit = "0"
#############################################################################

# SETUP GPIO PINS############################################################################
reed_pin = 40
Speaker = 38
GSMpower = 11
GSMreset = 12
GPIO_ButtonShutdown = 32
GPIO.setmode(GPIO.BOARD)

GPIO.setup(GPIO_ButtonShutdown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #system shutdown button
GPIO.add_event_detect(GPIO_ButtonShutdown, GPIO.RISING)

GPIO.setup(reed_pin, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(Speaker,GPIO.OUT)
GPIO.output(Speaker,0) #Initialize Speaker as off

GPIO.setup(GSMreset,GPIO.OUT)
GPIO.setup(GSMpower,GPIO.OUT)
GPIO.output(GSMpower,1) #Turn on GSM
GPIO.output(GSMreset,1) #Turn off GSM
GPIO.output(GSMreset,0) #Turn on GSM
##############################################################################

# INITIAL TIMER DATA #########################################################
start_program = 0
global timer
timer = 0 #initiate timer
timer_speed = 1
##############################################################################

# FUNCTIONS ###################################################################

def ShutdownPressed(arg):
    print("shutting down")
    os.system("sudo shutdown -h now")
    
def seat_belt_alert( textnumber):
    message = "Your child is unbuckled in a moving car!"
    GSMheader.StayorGoSMS(textnumber,message)

def warning_alert(textnumber):
    message = "Child has been left in car alone!"
    GSMheader.StayorGoSMS(textnumber,message)

def danger_temp_alert(textnumber):
    message = "Your child has been left alone in a hot car. Return to your car immediately!"
    GSMheader.StayorGoSMS(textnumber,message)
    
def temp_rate_alert(textnumber):
    message = "Your child has been left in the car, and the temperature is rising rapidly. Return to your car immediately!"
    GSMheader.StayorGoSMS(textnumber,message)
    
def EMS_warning_alert(textnumber):
    message = "Your child is still alone in a car after several alerts. Please return to your car immediately. EMS will be contacted in 60 seconds."
    GSMheader.StayorGoSMS(textnumber,message)
    
def parent_EMS_not(textnumber):
    message = "EMS has been contacted. Your child has been left in a car alone for an extended period of time. Please return to your car immediately!"
    GSMheader.StayorGoSMS(textnumber,message)

def EMS_call(callnumber,car_color, car_type, License_plate, Longitude, Latitude):
    GSMheader.FlushSerial()
    GSMerror = 0 # Keeps track of how many times GSM has thrown an error
    success = GSMheader.GSMcall(callnumber,car_color, car_type, License_plate, Longitude, Latitude) #Call and let us know if attempt was succesfull
    while True:
        if  success == 1:
            print("SMS successful. Total GSM errors: " + str(GSMerror))
            return GSMerror #Send updated GSM error count to Main function
            break #If Message was sent successully, continue with Main Code
        else:
            GSMheader.FlushSerial()
            GSMerror = GSMheader.GSMerrorfunc(GSMerror) #Update the GSMerror count
            success = GSMheader.GSMcall(callnumber,car_color, car_type, License_plate, Longitude, Latitude) #Resend text

def capture(flip_v = False, device = "/dev/spidev0.0"):
  with Lepton(device) as l:
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  #cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  #np.left_shift(a, 2, a)
  return np.int16(a)

def cameraTemp():
    global cameraTemp
    while(True):
        if __name__ == '__main__':
            
            cal_slope = float(.0247)
            lepton_temp = float(30565/100)- int(273)
            #print('cal factor {0}'.format(cal_slope))
            rawvalues = np.zeros(50)
            sum = np.zeros(50)
            
            for x in range(50):
            
                image = capture()
                #copy = image.copy()
                #copy = cv2.GaussianBlur(copy, (3, 3), 0)
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(image)
                #(minVal1, maxVal1, minLoc1, maxLoc1) = cv2.minMaxLoc(copy)
                scaled =  (cal_slope * (maxVal - 8192)) + lepton_temp
                rawvalues[x] = scaled
                #print(sum)
                sleep(.01)
                #cv2.imwrite("IMAGE.png", image)
            
            else:
                averaged = np.mean(sum)
                anotherone = np.mean(rawvalues)
                
##                print(" ")
##                print('Average raw value {}'.format(anotherone))
##                print('Averaged {}'.format(averaged))
##                print(" ")
                
                TempC = anotherone
                cameraTemp = TempC * 1.8 + 32 #Camera reading in degrees F.


def watchTemp (phonenum,backupnum,car_color,car_type,License_plate,Longitude,Latitude, first_alert, last_alert, base_temp, base_time, tempstart, danger_rate, maxtemp, child_base_temp, child_base_time, camera_start, child_danger_rate, camera_last_alert, camera_first_alert, child_maxtemp) :
    global connection_bit
    global timer
    global cameraTemp

    active = threading.active_count() #Count active threads
    i = 0 #Keep track if a temp alert has been sent
    left_alone_at = timer - base_time
    
    if active <= 4:
        warningSMS = threading.Thread(target = warning_alert ,args = (phonenum,))#send first warning text
        warningSMS.start()
        
    while True :
        active = threading.active_count() #Count active threads
        
        #calculate temperature alert parameters
        temperature = tempsensor.Temperature(base_temp, base_time, timer, tempstart, danger_rate, last_alert, first_alert, maxtemp)
        if timer < 3: cameraTemp = 97
        childTemperature = tempsensor.CameraTemperature(child_base_temp, child_base_time, timer, camera_start, child_danger_rate, camera_last_alert, camera_first_alert, child_maxtemp, cameraTemp)
        
        alone_time = timer - left_alone_at
        EMS_time = alone_time - first_alert

        print("Active Threads: " + str(active)) #If there are more than 3 active threads, the GSM is busy.
        print("Connection Bit: " + str(connection_bit))
        print("Primary Phone: " + str(phonenum))
        print("Backup Phone: " + str(backupnum))
        print("Car Color: " + str(car_color))
        print("Car Type: " + str(car_type))
        print("License Plate: " + str(License_plate))
        print("Last Known GPS Longitude: " + str(Longitude))
        print("Last Known GPS Latitude: " + str(Latitude))
        print("Child has been alone for : " + str(alone_time) + " seconds") #TEMPORARY
        
        if (temperature['danger_temp_bit'] | temperature['temp_rate_bit']) == 1 : #keep track of when first AMBIENT temp alert was made
            i = i + 1 #determine if a temperature alert has been sent

            if i == 1 : #only save time of first temperature alert once
                first_alert = temperature['last_alert'] #Save time of first temperature alert. Call for help in 4 min
            
            if temperature['danger_temp_bit'] == 1 & (active<=4): 
                dangertempSMS = threading.Thread(target = danger_temp_alert,args = (phonenum,)) #if car is at a dangerous temperature, send text.
                dangertempSMS.start()
            if temperature['temp_rate_bit'] == 1 & (active<=4):
                tempRateSMS = threading.Thread(target = temp_rate_alert ,args = (phonenum,)) #if car temp in increasing rapidly, send text.
                tempRateSMS.start() 

        if (childTemperature['camera_danger_temp_bit'] | childTemperature['camera_temp_rate_bit']) == 1 : #keep track of when first AMBIENT temp alert was made
            i = i + 1 #determine if a temperature alert has been sent

            if i == 1 : #only save time of first temperature alert once
                first_alert = childTemperature['camera_last_alert'] #Save time of first temperature alert. Call for help in 4 min
            
            if childTemperature['camera_danger_temp_bit'] == 1 & (active<=4): 
                dangertempSMS = threading.Thread(target = danger_temp_alert,args = (phonenum,)) #if car is at a dangerous temperature, send text.
                dangertempSMS.start()
            if childTemperature['camera_temp_rate_bit'] == 1 & (active<=4):
                tempRateSMS = threading.Thread(target = temp_rate_alert ,args = (phonenum,)) #if car temp in increasing rapidly, send text.
                tempRateSMS.start() 
        
        if (((EMS_time == 4*60) & (i>0)) & (active<=4)): #if child's been alone 4 min since first temp alert call EMS
            EMStempcalling = threading.Thread(target = EMS_call ,args = (EMSnum,car_color, car_type, License_plate, Longitude, Latitude))
            EMStempcalling.start()
            #Reset first and last temp alerts when call is attempted
            base_time = 0
            last_alert = 0  
            first_alert = 0
            break
            
        if (alone_time == 60*5) & (active<=4): #if child has been left in car for 5 min send warning text
            warningSMS2 = threading.Thread(target = warning_alert,args = (phonenum,))
            warningSMS2.start()
        
        if (((alone_time == 60*9) | ((EMS_time == 3*60) & (i>0))) & (active<=4)) : #if child has been left in safe temp car for 9 min or parent hasn't returned 3 min after first temp alert, tell parents that EMS is about to be contacted
            EMSwarningSMS = threading.Thread(target = EMS_warning_alert,args = (phonenum,))
            EMSwarningSMS.start()
        
        if (alone_time == 60*10) & (active<=4): #if child has ben left in car for 10 min , tell parents that EMS has been contacted and call EMS
            EMScalling = threading.Thread(target = EMS_call ,args = (EMSnum,car_color, car_type, License_plate, Longitude, Latitude))
            EMScalling.start()
            #Reset first and last temp alerts when call is attempted
            base_time = 0
            last_alert = 0  
            first_alert = 0
            break
            
        
        time.sleep(timer_speed) # wait for 1 second
        
        if connection_bit == "1" : # System begins recieving parent GPS Location, go back to checking if child is unbuckled in moving car
            print("App Reconnected")
            #Reset first and last temp alerts when parent returns (offbutton is pushed)
            base_time = 0
            last_alert = 0  
            first_alert = 0
            break

        #Update values
        base_temp = temperature['base_temp']
        base_time = temperature['base_time']
        tempstart = temperature['start']
        last_alert = temperature['last_alert']
        child_base_temp = childTemperature['child_base_temp']
        child_base_time = childTemperature['child_base_time']
        camera_start = childTemperature['camera_start']
        camera_last_alert = childTemperature['camera_last_alert']
        timer = timer + 1
        
    return {"first_alert" : first_alert, "last_alert" : last_alert, "base_temp" : base_temp, "base_time" : base_time, "tempstart" : tempstart, "Childtempstart" : Childtempstart}

def checkMovement(last_caralert, start_program, lastx, lasty, lastz, first_alert, last_alert, base_time, base_temp,tempstart, danger_rate, maxtemp, child_base_temp, child_base_time, camera_start, child_danger_rate, camera_last_alert, camera_first_alert, child_maxtemp):
    try:
        while (True):
            
            global phonenum
            global backupnum
            global car_color
            global car_type
            global License_plate
            global Longitude
            global Latitude
            global connection_bit
            global cameraTemp
            global timer

            print("\r\nCurrent time is: " +str(timer))
            print("Primary Phone: " + str(phonenum))
            print("Backup Phone: " + str(backupnum))
            print("Car Color: " + str(car_color))
            print("Car Type: " + str(car_type))
            print("License Plate: " + str(License_plate))
            print("Last Known GPS Longitude: " + str(Longitude))
            print("Last Known GPS Latitude: " + str(Latitude))
            print("Last seat belt alert time: " + str(last_alert))
            print("Camera temperature in degrees F: " + str(cameraTemp))
            print("Connection bit: " + str(connection_bit))
    
            moving = accel_sensor.Accelerometer_sensor(timer, GPIO.input(reed_pin), movingcar, last_caralert, start_program, lastx, lasty ,lastz)

            #Update accerometer/reed sensor/ alert values
            last_alert = moving['last_alert']
            start_program = moving['start_program']
            lastx = moving['lastx']
            lasty = moving['lasty']
            lastz = moving['lastz']

            if moving['reed_bit'] == 1 : #if child unbuckled in moving car, text parent
                GPIO.output(Speaker,1) #Turn on Speaker
            else: GPIO.output(Speaker,0) #Turn off Speaker

            if connection_bit == "0" : #Disconnected from App begin Temp/Timer alert procedure
                          
                #Update values
                checktemp = watchTemp(phonenum,backupnum,car_color,car_type,License_plate,Longitude,Latitude, first_alert, last_alert, base_temp, base_time, tempstart, danger_rate, maxtemp, child_base_temp, child_base_time, camera_start, child_danger_rate, camera_last_alert, camera_first_alert, child_maxtemp)
                first_alert = checktemp['first_alert']
                last_alert = checktemp['last_alert']
                base_temp = checktemp['base_temp']
                base_time = checktemp['base_time']
                tempstart = checktemp['tempstart']
                Childtempstart = checktemp['Childtempstart']
                last_alert = 0 # Reset seat belt last #Reset first and last temp alerts when parent returns (offbutton is pushed)
                BLElast_alert = 0  
                BLEfirst_alert = 0
            time.sleep(timer_speed)
            timer = timer + 1
    
    except StopIteration as err:
        print("GSM has thrown three errors. Check GSM. Exiting Main Procedure Code.")

def assigndata(data):
    global phonenum
    global backupnum
    global car_color
    global car_type
    global License_plate
    global Longitude
    global Latitude
    global connection_bit
    
    testsite_array = []
    for line in data:
        if line != "\n":
            testsite_array.append(line)
            if testsite_array[0] == "P" and testsite_array[-1] == '\r':
                phonenum = ''.join(testsite_array[1:-1]) #Combine array into string
 
            if testsite_array[0] == "B" and testsite_array[-1] == '\r':
                backupnum = ''.join(testsite_array[1:-1])
                
            if testsite_array[0] == "C" and testsite_array[-1] == '\r':
                car_color = ''.join(testsite_array[1:-1])
               
            if testsite_array[0] == "T" and testsite_array[-1] == '\r':
                car_type = ''.join(testsite_array[1:-1])
              
            if testsite_array[0] == "H" and testsite_array[-1] == '\r':
                License_plate = ''.join(testsite_array[1:-1])
              
            if testsite_array[0] == "O" and testsite_array[-1] == '\r':
                Longitude = ''.join(testsite_array[1:-1])
              
            if testsite_array[0] == "A" and testsite_array[-1] == '\r':
                Latitude = ''.join(testsite_array[1:-1])
                
            if testsite_array[0] == "R" and testsite_array[-1] == '\r':
                connection_bit = ''.join(testsite_array[1:-1])
        else:
                testsite_array = []
                     
def connected2App():  
    global connection_bit
    while (True):
        server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 1
        server_sock.bind(("",port))
        server_sock.listen(1)
        client_sock,address = server_sock.accept() #recieve phone's MAC
       
        if (address == ('50:77:05:A7:B3:99', 1)): #if connected to phone
            print"Accepted connection from ", address

            while (True):
                try:
                    connection_bit = "1"
                    assigndata(client_sock.recv(1024))
                    
                except:
                    print "App has disconnected"
                    address = 0 #reset address
                    connection_bit = "0"
                    break #break loop begin checking if phone has reconnected
        
    client_sock.close()
    server_sock.close()

        
###############START OF PROGRAM############################################
print("Current Temperature is: %.2f F" %tempsensor.readTempF())      
print("Maximum car temperature is: " + str(maxtemp))
# Create two threads as follows
GPIO.add_event_callback(GPIO_ButtonShutdown, ShutdownPressed)

try:
    thread1 = threading.Thread( target=checkMovement,name = 'Movement Check', args= (last_caralert, start_program, lastx, lasty, lastz, first_alert, last_alert, base_time, base_temp, tempstart, danger_rate, maxtemp, child_base_temp, child_base_time, camera_start, child_danger_rate, camera_last_alert, camera_first_alert, child_maxtemp))
##    thread2 = threading.Thread( target=connected2App,name = 'Bluetooth', args=() )

    thread1.start()
##    thread2.start()

    camerathread = threading.Thread( target=cameraTemp, args=() )
    camerathread.start()
   
except:
    print "Error: unable to start thread"

while 1: #Keep running threads
    time.sleep(0.1)
