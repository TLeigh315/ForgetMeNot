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

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

print("a")
message='AT'+'\r'
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv=port.read(20)
message=rcv.decode('utf-8')
print (rcv)
time.sleep(1)

print("b")
message='ATE0'+'\r' # Disable the Echo
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

print("c")
message='ATE0'+'\r' # Disable the Echo
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

print("d")
message='AT+CVHU=0'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

print("e")
message='ATI'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

print("f")
message='AT+GMM'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)
print("g")

message='AT+CPMS="SM","SM",SM"'
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)
print("h")

message='AT+CMGF=1'+'\r' # Select Message format as Text mode 
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

print("i")
message='AT+CNMI=2,1,0,0,0'+'\r'  # New SMS Message Indications
byte_message=message.encode('utf-8')
print(byte_message)
port.write(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

print("j")
message='AT+CMGS="18327978415"'+'\r'# Sending a message to a particular Number
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

print("k")
message='Your child has been left in the car alone. Please return to your car immediately.'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)

print("l")
message="\x1A" # Enable to send SMS
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
print("end")
for i in range(10):
    rcv = port.read(10)
    print (rcv)