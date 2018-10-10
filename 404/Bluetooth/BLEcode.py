import serial
import RPi.GPIO as GPIO      
import os, time
GPIO.setmode(GPIO.BOARD)    

# Enable Serial Communication
print("Begin Bluetooth procedure")
port = ("/dev/rfcomm1")
    
message='T32'+'\r'
byte_message=message.encode('utf-8')
print(byte_message)
port.echo(message)
rcv=port.read(20)
message=rcv.decode('utf-8')
print (rcv)
time.sleep(.5)

port.close()
