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
last_alert = 0
############################################################################

###########################################################################################
BLEstart_time = 0 #TEMPORARY
BLEtimer = BLEstart_time #inital timer value. Timer will be in seconds
BLElast_alert = 0 #time since last alert
danger_rate = 1.9
base_temp = 0
BLEbase_time = 0
temp_rate = 0 #difference between current and last temperature
BLEstart = 0 #will be zero only for timer = 1
#BLEtimer_speed = 1 #TEMPORARY timer iterates once/second USING timer_speed instead
max = 89 #maximum temperature
BLEfirst_alert= 0 #time of first alert
over = 0 # will allow program to end when EMS is called
#########################################################################################

############################################################################
##repeat = 5 #how many times voice call will run
##talk_delay = 10 #how long to wait before beginning to talk
testnum = "8327978415"
EMSnum = "8327978415"
phonenum = testnum
backupnum = "\r"
car_color = "\r"
car_type = "\r"
car_license = "\r"
Longitude = "\r"
Latitude = "\r"
#############################################################################

# SETUP GPIO PINS############################################################################
reed_pin = 36
GSMpower = 11
BLEonbutton = 40 #TEMPORARY onbutton represents parent leaving BLE range
BLEoffbutton= 38 #offbutton represents parent returning to BLE Range
GPIO.setmode(GPIO.BOARD)
GPIO.setup(reed_pin, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(BLEonbutton,GPIO.IN, GPIO.PUD_DOWN)  #TEMPORARY
GPIO.setup(BLEoffbutton,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(GSMpower,GPIO.OUT)
GPIO.output(GSMpower,1) #Turn on GSM
##############################################################################

# INITIAL TIMER DATA #########################################################
start_program = 0
timer = 0 #initiate timer
timer_speed = .5
##############################################################################
      
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

def EMS_call(callnumber,car_color, car_type, car_license, Longitude, Latitude):
    GSMheader.FlushSerial()
    GSMerror = 0 # Keeps track of how many times GSM has thrown an error
    success = GSMheader.GSMcall(callnumber,car_color, car_type, car_license, Longitude, Latitude) #Call and let us know if attempt was succesfull
    while True:
        if  success == 1:
            print("SMS successful. Total GSM errors: " + str(GSMerror))
            return GSMerror #Send updated GSM error count to Main function
            break #If Message was sent successully, continue with Main Code
        else:
            GSMheader.FlushSerial()
            GSMerror = GSMheader.GSMerrorfunc(GSMerror) #Update the GSMerror count
            success = GSMheader.GSMcall(callnumber,car_color, car_type, car_license, Longitude, Latitude) #Resend text

def STOP():     
    if GPIO.input(BLEoffbutton) == 1 : # If offbutton is pushed reset values and send program ending warning
        print("\r\n\r\nProgram offbutton pressed. Hold button for 3 seconds to end program")
        timer = 0
        last_alert = 0
        time.sleep(3)
    
        if GPIO.input(BLEoffbutton) == 1 : # If offbutton is pushed end program
            print("\r\n\r\nGoodbye!\n\n")
            return True
 
def watchTemp (BLEtimer,phonenum,backupnum,car_color,car_type,car_license,Longitude,Latitude, BLEfirst_alert, BLElast_alert, base_temp, BLEbase_time, BLEstart) :
    i = 0
    left_alone_at = BLEtimer - BLEbase_time
    while True :
        #calculate temperature alert parameters
        temperature = tempsensor.Temperature(base_temp, BLEbase_time, BLEtimer, BLEstart, danger_rate, BLElast_alert, BLEfirst_alert, max)
        alone_time = BLEtimer - left_alone_at
        EMS_time = alone_time - BLEfirst_alert

        print("Child has been alone for : " + str(alone_time) + " seconds") #TEMPORARY
        
        if (temperature['danger_temp_bit'] | temperature['temp_rate_bit']) == 1 : #keep track of when first alert was made
            i = i + 1 #determine if a temperature alert has been sent

            if i == 1 : #only save time of first temperature alert once
                BLEfirst_alert = temperature['last_alert'] #Save time of first temperature alert. Call for help in 4 min
            
            if temperature['danger_temp_bit'] == 1: 
                dangertempSMS = threading.Thread(target = danger_temp_alert,args = (testnum,)) #if car is at a dangerous temperature, send text.
                dangertempSMS.start()
            if temperature['temp_rate_bit'] == 1 :
                temprateSMS = threading.Thread(target = temp_rate_alert ,args = (testnum,)) #if car temp in increasing rapidly, send text.
                temprateSMS.start()
 
        if ((EMS_time == 4*60) & (i>0)) : #if child's been alone 4 min since first temp alert call EMS
            EMScalling = threading.Thread(target = EMS_call ,args = (EMSnum,car_color, car_type, car_license, Longitude, Latitude))
            EMScalling.start()
            break
            
        if (alone_time == 60*5) : #if child has been left in car for 5 min send warning text
            warningSMS2 = threading.Thread(target = warning_alert,args = (testnum,))
            warningSMS2.start()
        if ((alone_time == 60*9) | ((EMS_time == 3*60) & (i>0))) : #if child has been left in safe temp car for 9 min or parent hasn't returned 3 min after first temp alert, tell parents that EMS is about to be contacted
            EMSwarningSMS = threading.Thread(target = EMS_warning_alert,args = (testnum,))
            EMSwarningSMS.start()
        if (alone_time > 60*10) : #if child has ben left in car for 10 min , tell parents that EMS has been contacted and call EMS
            EMScalling = threading.Thread(target = EMS_call ,args = (EMSnum,car_color, car_type, car_license, Longitude, Latitude))
            EMScalling.start()
            break
        
        time.sleep(timer_speed) # wait for 1 second
        
        if GPIO.input(BLEoffbutton) == 1 : # System begins recieving parent GPS Location, go back to checking if child is unbuckled in moving car
            print("App Reconnected")
            #Reset first and last temp alerts when parent returns (offbutton is pushed)
            BLElast_alert = 0  
            BLEfirst_alert = 0
            break

        #Update values
        base_temp = temperature['base_temp']
        BLEbase_time = temperature['base_time']
        BLEstart = temperature['start']
        BLElast_alert = temperature['last_alert']
        BLEtimer = BLEtimer + 1
        
    return {"BLEtimer" : BLEtimer, "BLEfirst_alert" : BLEfirst_alert, "BLElast_alert" : BLElast_alert, "base_temp" : base_temp, "BLEbase_time" : BLEbase_time, "BLEstart" : BLEstart}

def checkMovement(phonenum,backupnum,car_color,car_type,car_license,Longitude,Latitude,timer, last_alert, start_program, lastx, lasty, lastz, BLEfirst_alert, BLElast_alert, BLEbase_time, base_temp):
    try:
        while (True):
            print("\r\nCurrent time is: " +str(timer))
        

            #Update contact and calling information
##            if App_phonenum == "\r": phonenum = phonenum
##            else:
##                phonenum = App_phonenum
##                print("Primary Phone: " + str(phonenum))
##            
##            if App_backupnum == "\r": backupnum = backupnum
##            else:
##                backupnum = App_backupnum
##                print("Backup Phone: " + str(App_backupnum))
##            
##            if App_car_color == "\r": car_color = car_color
##            else:
##                car_color = App_car_color
##                print("Car Color: " + str(car_color))
##            
##            if App_car_type == "\r": car_type = car_type
##            else:
##                car_type = App_car_type
##                print("Car Type: " + str(car_type))
##            
##            if App_car_license == "\r": car_license = car_license
##            else:
##                car_license = App_car_license
##                print("License Plate: " + str(car_license))
##
##            if App_Longitude == "\r":
##                Longitude = Longitude
##                print("Last Known GPS Longitude: " + str(Longitude))
##            else:
##                Longitude = App_Longitude
##                print("GPS Longitude: " + str(App_Longitude))
##
##            if App_Latitude == "\r":
##                Latitude = Latitude
##                print("Last Known GPS Latitude: " + str(Latitude))
##            else:
##                Latitude = App_Latitude
##                print("GPS Latitude: " + str(App_Latitude))

            #Begin checking if child is unbuckled in moving car
            print("Last seat belt alert time: " + str(last_alert))
    
            moving = accel_sensor.Accelerometer_sensor(timer, GPIO.input(reed_pin), movingcar, last_alert, start_program, lastx, lasty ,lastz)

            #Update accerometer/reed sensor/ alert values
            last_alert = moving['last_alert']
            start_program = moving['start_program']
            lastx = moving['lastx']
            lasty = moving['lasty']
            lastz = moving['lastz']

            if moving['reed_bit'] == 1 : #if child unbuckled in moving car, text parent
                threading.Thread(target = seat_belt_alert ,args = (testnum,))
        
            if GPIO.input(BLEonbutton) == 1 : #Disconnected from App begin Temp/Timer alert procedure
                warningSMS = threading.Thread(target = warning_alert ,args = (testnum,))#send first warning text
                warningSMS.start()
                
                #Update values
                checktemp = watchTemp(timer, phonenum,backupnum,car_color,car_type,car_license,Longitude,Latitude, BLEfirst_alert, BLElast_alert, base_temp, BLEbase_time, BLEstart)
                BLEfirst_alert = checktemp['BLEfirst_alert']
                BLElast_alert = checktemp['BLElast_alert']
                BLEbase_time = checktemp['BLEbase_time']
                base_temp = checktemp['base_temp']
                timer = checktemp['BLEtimer']
                last_alert = 0 # Reset seat belt last #Reset first and last temp alerts when parent returns (offbutton is pushed)
                BLElast_alert = 0  
                BLEfirst_alert = 0
            if STOP() == True: break
            time.sleep(timer_speed)
            timer = timer + 1
    
    except StopIteration as err:
        print("GSM has thrown three errors. Check GSM. Exiting Main Procedure Code.")

def assigndata(data,phonenum,backupnum,car_color,car_type,car_license,Longitude,Latitude):
                    
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
              
            if testsite_array[0] == "L" and testsite_array[-1] == '\r':
                car_license = ''.join(testsite_array[1:-1])
              
            if testsite_array[0] == "O" and testsite_array[-1] == '\r':
                Longitude = ''.join(testsite_array[1:-1])
              
            if testsite_array[0] == "A" and testsite_array[-1] == '\r':
                Latitude = ''.join(testsite_array[1:-1])

        else:
                testsite_array = []

    return {'phonenum':phonenum, 'backupnum':backupnum, 'car_color':car_color, 'car_type':car_type, 'car_license':car_license, 'Longitude':Longitude, 'Latitude':Latitude}
                       
def connected2App(phonenum,backupnum,car_color,car_type,car_license,Longitude,Latitude):  
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
                    data = client_sock.recv(1024)
                    print(data)
                    assigndata(data,phonenum,backupnum,car_color,car_type,car_license,Longitude,Latitude)

                    
                except:
                    print "App has disconnected"
                    address = 0 #reset address
                    stop = input("Try again? [Y=1 and N=2]")
                    break #break loop begin checking if phone has reconnected
                if GPIO.input(BLEoffbutton) == 1: break

        if stop == 2: break
        
    client_sock.close()
    server_sock.close()

        
###############START OF PROGRAM############################################
print("Current Temperature is: %.2f F" %tempsensor.readTempF())      
print("Maximum car temperature is: " + str(max))
# Create two threads as follows
##from multiprocessing.pool import ThreadPool
##pool = ThreadPool(processes=1)
from threading import Thread
import threading
import time
import random
from Queue import Queue
    
try:
    thread1 = threading.Thread( target=checkMovement,name = 'Movement Check', args= (phonenum,backupnum,car_color,car_type,car_license,Longitude,Latitude, timer, last_alert, start_program, lastx, lasty, lastz, BLEfirst_alert, BLElast_alert, BLEbase_time, base_temp) )
##    thread2 = threading.Thread( target=connected2App, args=(phonenum,backupnum,car_color,car_type,car_license,Longitude,Latitude) )

    thread1.start()
##    thread2.start()
##    thread1.join()

##    print("\n\nCurrent Active Thread Count\n\n")
##    print(threading.activeCount())
##    thread2.join()
##
##    print("\n\n\nThread Count is:")
##    print(threading.activeCount())
##    

except:
    print "Error: unable to start thread"

while 1: #Keep running threads
    pass
