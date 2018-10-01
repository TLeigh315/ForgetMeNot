import serial
import RPi.GPIO as GPIO      
import os, time

GPIO.setmode(GPIO.BOARD)    

# Enable Serial Communication
print("start")
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

#Flush Serial
print("flush\n")
port.flushInput()
time.sleep(1)
port.flushOutput()
time.sleep(1)

print("a")
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key
message='AT'+'\r\n'
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv=port.read(10)
message=rcv.decode('utf-8')
print (rcv)
time.sleep(1)

print("b")
message='ATE0'+'\r\n'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
#port.write('ATE0'+'\r\n')      # Disable the Echo
rcv = port.read(10)
print (rcv)
time.sleep(1)
print("c")

message='ATE0'+'\r\n'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
#port.write('ATE0'+'\r\n')      # Disable the Echo
rcv = port.read(10)
print (rcv)
time.sleep(1)
print("d")

message='AT+CVHU=0'+'\r\n'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
#port.write('ATE0'+'\r\n')      # Disable the Echo
rcv = port.read(10)
print (rcv)
time.sleep(1)
print("e")

message='ATI'+'\r\n'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
#port.write('ATE0'+'\r\n')      # Disable the Echo
rcv = port.read(15)
print (rcv)
time.sleep(1)
print("f")

message='AT+GMM'+'\r\n'
byte_message=message.encode('utf-8')
#port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
port.write(byte_message)
print(byte_message)
rcv = port.read(15)
print (rcv)
time.sleep(1)
print("g")

message='AT+CPMS="SM","SM",SM"'
#message='AT+CNMI=2,1,0,0,0'+'\r\n'
byte_message=message.encode('utf-8')
print(byte_message)
#port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
port.write(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)
print("h")

message='AT+CMGF=1'+'\r\n'
byte_message=message.encode('utf-8')
#port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
port.write(byte_message)
print(byte_message)
rcv = port.read(10)
print (rcv)
time.sleep(1)
print("i")
# Sending a message to a particular Number

message='AT+CMGS="8327978415"'+'\r\n'
byte_message=message.encode('utf-8')
#port.write('AT+CMGS="9495353464"'+'\r\n')
port.write(byte_message)
print(byte_message)
rcv = port.read(10)
print (rcv)
time.sleep(1)
print("j")

message='Hello User'+'\r\n'
byte_message=message.encode('utf-8')
#port.write('Hello User'+'\r\n')  # Message
port.write(byte_message)
print(byte_message)
rcv = port.read(10)
print (rcv)
print("k")

message="\x1A"
byte_message=message.encode('utf-8')
#port.write("\x1A") # Enable to send SMS
port.write(byte_message)
print(byte_message)
print("end")
for i in range(10):
    rcv = port.read(10)
    print (rcv)