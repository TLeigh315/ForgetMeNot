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
rcv=port.read(10)
message=rcv.decode('utf-8')
print (rcv)
time.sleep(1)

print("b")
message='ATE0'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(10)
print (rcv)
time.sleep(1)

print("c")
message='ATE0'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(10)
print (rcv)
time.sleep(1)

print("d")
message='AT+CVHU=0'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(10)
print (rcv)
time.sleep(1)

print("e")
message='ATI'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(25)
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
message='AT+CPMS="SM","SM",SM"'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

print("h")
message='AT+COPS?'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(50)
print (rcv)
time.sleep(1)

print("h")
message='ATZ'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(10)
print (rcv)
time.sleep(1)

print("h")
message='AT+CUSD=1'+'\r' #Allows control of the Unstructered Supplementary Service Data
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(10)
print (rcv)
time.sleep(1)

print("i")
message='ATD+18327978415;'+'\r'
byte_message=message.encode('utf-8')
port.write(byte_message)
print(byte_message)
rcv = port.read(20)
print (rcv)
time.sleep(1)

while(1):
    print(port.readline())

time.sleep(1)

    
print("end")


