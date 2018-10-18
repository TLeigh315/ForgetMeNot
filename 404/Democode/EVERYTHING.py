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
repeat = 5 #how many times voice call will run
talk_delay = 10 #how long to wait before beginning to talk
car_color = "black"
car_type = "Nissan Versa"
car_license = "AFD3243"
Longitude = 33.354
Long_Dir = "North"
Latitude = 56.244
Lat_Dir = "East"
phonenum = "8327978415"
backupnum = "8327978415"
EMSnum = "8327978415"
#############################################################################

# SETUP GPIO PINS############################################################################
reed_pin = 36
GSMpower = 11
BLEonbutton = 40 #onbutton represents parent leaving BLE range
BLEoffbutton= 38 #offbutton represents parent returning to BLE Range
GPIO.setmode(GPIO.BOARD)
GPIO.setup(reed_pin, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(BLEonbutton,GPIO.IN, GPIO.PUD_DOWN) 
GPIO.setup(BLEoffbutton,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(GSMpower,GPIO.OUT)
GPIO.output(GSMpower,1) #Turn on GSM
##############################################################################

# INITIAL TIMER DATA #########################################################
start_program = 0
timer = 0 #initiate timer
timer_speed = 1
##############################################################################

# Enable Serial Communication with GSM
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1) #Declare what serial port to use

# Define/Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GSMreset = 12
GPIO.setup(GSMreset,GPIO.OUT)
       

def FlushSerial():
    port.flushInput()
    time.sleep(.5)
    port.flushOutput()
    time.sleep(.5)

def GSMconvo( message):
    sendGSM = message + '\r' #Change original message into GSM message format
    print(sendGSM.encode('utf-8')) #encode message and print to terminal
    port.write(sendGSM.encode('utf-8')) #encode message and send to serial port
    port.readline() #This WILL be '\r\n'. Need line to read GSM response on next line
    rcv=port.readline()
    print (rcv) #Read and print GSM response to terminal
    time.sleep(.5)
    if rcv == "ERROR\r\n": raise ValueError("Returning to the GSM function")
  
def GSMsms (textnumber, textmessage):
    try:
        # Transmitting AT Commands to the Modem
        GSMconvo('AT')
        GSMconvo('ATE0') # Disable the Echo
        GSMconvo('ATE0') # Disable the Echo
        GSMconvo('AT+CVHU=0')
        GSMconvo('ATI')
        GSMconvo('AT+GMM')
        GSMconvo('AT+CPMS="SM","SM","SM"')
        GSMconvo('AT+CSCS="GSM"')
        GSMconvo('AT+CMGF=1') # Select Message format as Text mode 
        GSMconvo('AT+CNMI=2,1,0,0,0') # New SMS Message Indications
        GSMconvo('AT+CMGS="1'+ textnumber +'"') # Determine what number to text
        GSMconvo(textmessage) #Determine content of text
        GSMconvo("\x1A") # Enable to send SMS
        return 1 #Let us know if SMS text was successfull

    except ValueError as err:
        return 0 #Let us know if SMS text failed

def GSMcall (callnumber, car_color, car_type, car_license, Longitude, Latitude):
    try:
        # Transmitting AT Commands to the Modem
        GSMconvo('AT')
        GSMconvo('ATE0') # Disable the Echo
        GSMconvo('ATE0') # Disable the Echo
        GSMconvo('AT+CVHU=0')
        GSMconvo('ATI')
        GSMconvo('AT+GMM')
        GSMconvo('AT+CPMS="SM","SM","SM"')
        GSMconvo('ATZ')
        GSMconvo('AT+CUSD=1') #Allows control of the Unstructered Supplementary Service Data
        GSMconvo('ATD+1' + callnumber + ';') # Determine what number to call
        EMScaller(car_color, car_type, car_license, Longitude, Latitude)     
        return 1 #Let us know if call was successfull

    except ValueError as err:
        return 0 #Let us know if call failed     
    
def GSMerrorfunc(GSMerror):
    GPIO.output(GSMreset,1) #Reset GSM
    GPIO.output(GSMreset,0) #Turn on GSM
    GSMerror = GSMerror + 1 #Keep track of how many times GSM has thrown error
    if GSMerror >= 3:
        raise StopIteration("Too many GSM errors. Quit trying to use GSM")

    print("GSM has thrown " + str(GSMerror) + " error(s) \n\n\n")
    FlushSerial()
    time.sleep(5) #Allow time for GSM to power back on
    return GSMerror #Send updated GSM error count to other functions

def StayorGoSMS(textnumber,message):
    FlushSerial()
    GSMerror = 0 # Keeps track of how many times GSM has thrown an error
    success = GSMsms(textnumber,message) #Send SMS Text and let us know if attempt was succesfull
    while True:
        if  success == 1:
            print("SMS successful. Total GSM errors: " + str(GSMerror))
            return GSMerror #Send updated GSM error count to Main function
            break #If Message was sent successully, continue with Main Code
        else:
            FlushSerial()
            GSMerror = GSMerrorfunc(GSMerror) #Update the GSMerror count
            success = GSMsms(textnumber,message) #Resend text
     
def seat_belt_alert( textnumber):
    message = "Your child is unbuckled in a moving car!"
    StayorGoSMS(textnumber,message)

def warning_alert(textnumber):
    message = "Child has been left in car alone!"
    StayorGoSMS(textnumber,message)

def danger_temp_alert(textnumber):
    message = "Your child has been left alone in a hot car. Return to your car immediately!"
    StayorGoSMS(textnumber,message)
    
def temp_rate_alert(textnumber):
    message = "Your child has been left in the car, and the temperature is rising rapidly. Return to your car immediately!"
    StayorGoSMS(textnumber,message)
    
def EMS_warning_alert(textnumber):
    message = "Your child is still alone in a car after several alerts. Please return to your car immediately. EMS will be contacted in 60 seconds."
    StayorGoSMS(textnumber,message)
    
def parent_EMS_not(textnumber):
    message = "EMS has been contacted. Your child has been left in a car alone for an extended period of time. Please return to your car immediately!"
    StayorGoSMS(textnumber,message)

def EMS_call(callnumber,car_color, car_type, car_license, Longitude, Latitude):
    FlushSerial()
    GSMerror = 0 # Keeps track of how many times GSM has thrown an error
    success = GSMcall(callnumber,car_color, car_type, car_license, Longitude, Latitude) #Call and let us know if attempt was succesfull
    while True:
        if  success == 1:
            print("SMS successful. Total GSM errors: " + str(GSMerror))
            return GSMerror #Send updated GSM error count to Main function
            break #If Message was sent successully, continue with Main Code
        else:
            FlushSerial()
            GSMerror = GSMerrorfunc(GSMerror) #Update the GSMerror count
            success = GSMcall(callnumber,car_color, car_type, car_license, Longitude, Latitude) #Resend text

def RpiSays(words_to_speak):
    words_to_speak = str(words_to_speak)
    #Replacing ' ' with '_' to identify words in the text entered
    words_to_speak = words_to_speak.replace(' ', '_')

    cmd_beg= 'espeak -ven+f4 -g10 -s150'
    cmd_end= ' 2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
    cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file
    call([cmd_beg+cmd_out+words_to_speak+cmd_end], shell=True)

def militaryABC(letter):
    convert_letter = {
        "A" : "Alfa",
        "B" : "Bravo",
        "C" : "Charlie",
        "D" : "Delta",
        "E" : "Echo",
        "F" : "Foxtrot",
        "G" : "Golf",
        "H" : "Hotel",
        "I" : "India",
        "J" : "Juliett",
        "K" : "Kilo",
        "L" : "Lima",
        "M" : "Mike",
        "N" : "November",
        "O" : "Oscar",
        "P" : "Papa",
        "Q" : "Quebec",
        "R" : "Romeo",
        "S" : "Sierra",
        "T" : "Tango",
        "U" : "Uniform",
        "V" : "Victor",
        "W" : "Whiskey",
        "X" : "Xray",
        "Y" : "Yankee",
        "Z" : "Zulu",
        "1" : "One",
        "2" : "Two",
        "3" : "Three",
        "4" : "Four",
        "5" : "Five",
        "6" : "Six",
        "7" : "Seven",
        "8" : "Eight",
        "9" : "Nine",
        "0" : "Zero"
    }
    return convert_letter.get(letter, "Invalid Letter")
        
def EMScaller(car_color, car_type, car_license, Longitude, Latitude):
    pygame.mixer.init(frequency=48500, size=-16, channels = 2, buffer = 4096)
    pygame.init()
    pygame.mixer.init()
    Intro = pygame.mixer.Sound("Intro.wav")
    Car_Intro = pygame.mixer.Sound("Car_Description.wav")
    GPS_Intro = pygame.mixer.Sound("At_GPS_Location.wav")
    East = pygame.mixer.Sound("Degrees_East.wav")
    West = pygame.mixer.Sound("Degrees_West.wav")
    North = pygame.mixer.Sound("Degrees_North.wav")
    South = pygame.mixer.Sound("Degrees_South.wav")
    And = pygame.mixer.Sound("And.wav")
    License_Plate_Intro = pygame.mixer.Sound("License_Plate_Intro.wav")

    Intro.play()
    time.sleep(9)

    Car_Intro.play()
    time.sleep(3)

    RpiSays(car_color)
    RpiSays(car_type)

    License_Plate_Intro.play()
    time.sleep(2.5)
    for letter in car_license:
        RpiSays(militaryABC(letter))
        time.sleep(.5)

    GPS_Intro.play()
    time.sleep(3)
       

    if Longitude < 0:
        RpiSays(Longitude*-1)
        South.play()
    else:
        RpiSays(Longitude)
        North.play()
    time.sleep(1.5)

    And.play()
    time.sleep(2)

    if Latitude < 0:
        RpiSays(Latitude*-1)
        West.play()
    else:
        RpiSays(Latitude)
        East.play()
    time.sleep(2)
    pygame.display.quit()
    pygame.quit()

def STOP():     
    if GPIO.input(BLEoffbutton) == 1 : # If offbutton is pushed reset values and send program ending warning
        print("\r\n\r\nProgram offbutton pressed. Hold button for 3 seconds to end program")
        timer = 0
        last_alert = 0
        time.sleep(3)
    
        if GPIO.input(BLEoffbutton) == 1 : # If offbutton is pushed end program
            print("\r\n\r\nGoodbye!\n\n")
            return True
 
def assigndata(data):
    testsite_array = []
    for line in data:
        if line != "\n":
            testsite_array.append(line)
            if testsite_array[0] == "P" and testsite_array[-1] == '\r':
                phonenum = ''.join(testsite_array[1:-1])
                print("Primary Phone: " + phonenum)
                
            if testsite_array[0] == "B" and testsite_array[-1] == '\r':
                backupnum = ''.join(testsite_array[1:-1])
                print("Backup Phone: " + backupnum)
                
            if testsite_array[0] == "C" and testsite_array[-1] == '\r':
                car_color = ''.join(testsite_array[1:-1])
                print("Car Color: " + car_color)
                
            if testsite_array[0] == "T" and testsite_array[-1] == '\r':
                car_type = ''.join(testsite_array[1:-1])
                print("Car Type: " + car_type)
                
            if testsite_array[0] == "L" and testsite_array[-1] == '\r':
                car_license = ''.join(testsite_array[1:-1])
                print("License Plate: " + car_license)
                
            if testsite_array[0] == "O" and testsite_array[-1] == '\r':
                Longitude = ''.join(testsite_array[1:-1])
                print("GPS Longitude: " + Longitude)
                
            if testsite_array[0] == "A" and testsite_array[-1] == '\r':
                Latitude = ''.join(testsite_array[1:-1])
                print("GPS Latitude: " + Latitude)
        else:
                testsite_array = []

                
def watchTemp (BLEtimer, BLEfirst_alert, BLElast_alert, base_temp, BLEbase_time, BLEstart) :
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

            if i == 1 : #only save first alert once
                BLEfirst_alert = temperature['last_alert']
            
            if temperature['danger_temp_bit'] == 1: 
                danger_temp_alert(phonenum)

            if temperature['temp_rate_bit'] == 1 :
                temp_rate_alert(phonenum)
 
                
        if ((EMS_time == 4*60) & (i>0)) : #if child's been alone 4 min since first temp alert call EMS
            EMS_call(phonenum,car_color, car_type, car_license, Longitude, Latitude)
            over = 1
            
        if (alone_time == 60*5) : #if child has been left in car for 5 min send warning text
            warning_alert(phonenum)
        
        if ((alone_time == 60*9) | ((EMS_time == 3*60) & (i>0))) : #if child has been left in safe temp car for 9 min or parent hasn't returned 3 min after first temp alert, tell parents that EMS is about to be contacted
            EMS_warning_alert(phonenum)
        
        if (alone_time > 60*10) : #if child has ben left in car for 10 min , tell parents that EMS has been contacted and call EMS
            EMS_call(EMSnum,car_color, car_type, car_license, Longitude, Latitude)
            over = 1
            break
        
        time.sleep(timer_speed) # wait for ___ seconds
        

        if GPIO.input(BLEoffbutton) == 1 : # If offbutton is pushed (parent returns within BLE range)
            print("BLEoffbutton Pressed")
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
    
def connected2App():  
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
                    assigndata(client_sock.recv(1024))
                    
                except:
                    print "App has disconnected"
                    address = 0 #reset address
                    stop = input("Try again? [Y=1 and N=2]")
                    break #break loop begin checking if phone has reconnected
            if stop == 2: break
        
    client_sock.close()
    server_sock.close()
    print "Program finished."

def checkMovement(timer, last_alert, start_program, lastx, lasty, lastz, BLEfirst_alert, BLElast_alert, BLEbase_time, base_temp):
    try:
        while (True):
            print("\r\nCurrent time is: " +str(timer))
            print("Last seat belt alert time: " + str(last_alert))

            moving = accel_sensor.Accelerometer_sensor(timer, GPIO.input(reed_pin), movingcar, last_alert, start_program, lastx, lasty ,lastz)

            #Update values
            last_alert = moving['last_alert']
            start_program = moving['start_program']
            lastx = moving['lastx']
            lasty = moving['lasty']
            lastz = moving['lastz']

            if moving['reed_bit'] == 1 : #if child unbuckled in moving car, text parent
                seat_belt_alert(phonenum)

            if (GPIO.input(BLEonbutton)): #Disconnected from App begin Temp/Timer alert procedure
                print("OnButton Pressed")
                thread.start_new_thread(warning_alert , (phonenum,))#send first warning text
            
                #Update values
                checktemp = watchTemp(timer, BLEfirst_alert, BLElast_alert, base_temp, BLEbase_time, BLEstart)
                BLEfirst_alert = checktemp['BLEfirst_alert']
                BLElast_alert = checktemp['BLElast_alert']
                BLEbase_time = checktemp['BLEbase_time']
                base_temp = checktemp['base_temp']
                timer = checktemp['BLEtimer']
                last_alert = 0 # Reset seat belt last #Reset first and last temp alerts when parent returns (offbutton is pushed)
                BLElast_alert = 0  
                BLEfirst_alert = 0
            

            time.sleep(timer_speed)
            timer = timer + 1

            if STOP() == True:
                break

    
    except StopIteration as err:
        print("GSM has thrown three errors. Check GSM. Exiting Main Procedure Code.")
        
    
###############START OF PROGRAM############################################
print("Current Temperature is: %.2f F" %tempsensor.readTempF())      
print("Maximum car temperature is: " + str(max))
# Create two threads as follows

try:
    thread.start_new_thread( checkMovement,(timer, last_alert, start_program, lastx, lasty, lastz, BLEfirst_alert, BLElast_alert, BLEbase_time, base_temp) )
    thread.start_new_thread(connected2App , () )
except:
    print "Error: unable to start thread"

while 1:
    pass
