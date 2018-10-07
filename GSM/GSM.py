import serial
import RPi.GPIO as GPIO      
import os, time

textnumber = '8327978415'
textmessage = 'Your child has been left in the car alone. Please return to your car immediately.'
GPIO.setmode(GPIO.BOARD)    

# Enable Serial Communication
print("Begin SMS procedure")
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

#Flush Serial
port.flushInput()
time.sleep(.5)
port.flushOutput()
time.sleep(.5)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

message='AT'+'\r'
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv=port.read(20)
message=rcv.decode('utf-8')
print (rcv)
time.sleep(.5)

message='ATE0'+'\r' # Disable the Echo
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message='ATE0'+'\r' # Disable the Echo
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message='AT+CVHU=0'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message='ATI'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message='AT+GMM'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message='AT+CPMS="SM","SM",SM"'
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message='AT+CSCS="GSM"'+'\r' # Select Message format as Text mode 
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

message='AT+CMGF=1'+'\r' # Select Message format as Text mode 
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message='AT+CNMI=2,1,0,0,0'+'\r'  # New SMS Message Indications
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message='AT+CMGS="1'+textnumber+'"\r'# Sending a message to a particular Number
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message = textmessage
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(.5)

message="\x1A" # Enable to send SMS
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
for i in range(10):
    rcv = port.read(10)
    print (rcv)
    
port.close()