import serial
import RPi.GPIO as GPIO      
import os, time

textnumber = '8327978415'
textmessage = 'Please return to your car immediately!'
GPIO.setmode(GPIO.BOARD)    

# Enable Serial Communication
print("Begin SMS procedure")
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1) #Declare what serial port to use

#Flush Serial
port.flushInput()
time.sleep(.5)
port.flushOutput()
time.sleep(.5)

# Transmitting AT Commands to the Modem
def GSMconvo(message):
    sendGSM = message + '\r' #Change original message into GSM message format
    print(sendGSM.encode('utf-8')) #encode message and print to terminal
    port.write(sendGSM.encode('utf-8')) #encode message and send to serial port
    port.readline() #This WILL be '\r\n'. Need line to read GSM response on next line
    print (port.readline()) #Read and print GSM response to terminal
    time.sleep(.5)
    
GSMconvo('AT')
GSMconvo('ATE0') # Disable the Echo
GSMconvo('ATE0') # Disable the Echo
GSMconvo('AT+CVHU=0')
GSMconvo('ATI')
GSMconvo('AT+GMM')
GSMconvo('AT+CPMS="SM","SM",SM"')
GSMconvo('AT+CSCS="GSM"')
GSMconvo('AT+CMGF=1') # Select Message format as Text mode 
GSMconvo('AT+CNMI=2,1,0,0,0') # New SMS Message Indications
GSMconvo('AT+CMGS="1'+ textnumber +'"') # Determine what number to text
GSMconvo(textmessage) #Determine content of text
GSMconvo("\x1A") # Enable to send SMS
port.close()