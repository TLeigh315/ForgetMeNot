import RPi.GPIO as GPIO
import smbus
import time
import serial
import pygame
from subprocess import call

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
    textnumber = str(textnumber)
    textmessage = str(textmessage)
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

    for repeat in range(0,5):
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
            time.sleep(.3)

        GPS_Intro.play()
        time.sleep(3)
           

        if int(Longitude) < 0:
            RpiSays(Longitude*(-1))
            South.play()
        else:
            RpiSays(Longitude)
            North.play()
        time.sleep(1.5)

        And.play()
        time.sleep(2)

        if int(Latitude) < 0:
            RpiSays(Latitude*(-1))
            West.play()
        else:
            RpiSays(Latitude)
            East.play()
        time.sleep(2)
    pygame.display.quit()
    pygame.quit()

  


