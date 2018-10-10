import serial
import RPi.GPIO as GPIO      
import os, time

textnumber = '8327978415'
textmessage = 'Please return to your car immediately!.'
GPIO.setmode(GPIO.BOARD)    

# Enable Serial Communication
print("Begin SMS procedure")
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

# Transmitting AT Commands to the Modem
# '\r' indicates the Enter key


message='AT'+'\r'
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv14=port.readline() #WHY ISN'T AT GETTING A RESPONSE?
print (rcv14)
time.sleep(.5)

if rcv14 == '\r\n': #if AT doesn't get a response, send AT Command again.
    print("BLANKLINE")
    message='AT'+'\r'
    byte_message=message.encode('utf-8')
    print(byte_message)
    port.write(byte_message)
    rcv15=port.readline() #WHY ISN'T AT GETTING A RESPONSE?
    print (rcv15)
    time.sleep(.5)
    if rcv15 == "OK\r\n":
        print("received the OK!")

message='ATE0'+'\r' # Disable the Echo
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv1 = port.readline()
#print (rcv1)
time.sleep(.5)

message='ATE0'+'\r' # Disable the Echo
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv2 = port.readline()
#print (rcv2) #WHY ISN'T AT GETTING A RESPONSE?
time.sleep(.5)

message='AT+CVHU=0'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv3 = port.readline()
#print (rcv3)
time.sleep(.5)

message='ATI'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv4 = port.readline()
#print (rcv4) #WHY ISN'T AT GETTING A RESPONSE?
time.sleep(.5)

message='AT+GMM'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv5 = port.readline()
#print (rcv5)
time.sleep(.5)

message='AT+CPMS="SM","SM",SM"'
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv6 = port.readline()
#print (rcv6)
time.sleep(.5)

message='AT+CSCS="GSM"'+'\r' # Select Message format as Text mode 
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv7 = port.readline()
#print (rcv7)
time.sleep(1)

message='AT+CMGF=1'+'\r' # Select Message format as Text mode 
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv8 = port.readline()
#print (rcv8)
time.sleep(.5)

message='AT+CMGF=1'+'\r' # Select Message format as Text mode 
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv8 = port.readline()
#print (rcv8)
time.sleep(.5)

message='AT+CNMI=2,1,0,0,0'+'\r'  # New SMS Message Indications
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv13 = port.readline()
#print (rcv9=13)
time.sleep(.5)

message='AT+CMGS="1'+textnumber+'"\r'# Sending a message to a particular Number
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv10 = port.readline()
#print (rcv10)
time.sleep(.5)

message = textmessage
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv11 = port.readline()
#print (rcv11)
time.sleep(.5)

message="\x1A" # Enable to send SMS
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv12 = port.readline()
#print (rcv12)
time.sleep(.5)
    
port.close()