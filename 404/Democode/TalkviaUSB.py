import serial
import time
import subprocess
dev = subprocess.check_output('ls /dev/ttyACM*', shell=True) #find out what name the Arduino is under
print (dev) #display Arduino name (will be shown in bytes)
dev=dev.decode("utf-8") #convert Arduino name from bytes to string
dev=dev.replace("\n","") #get ride of \n
try:
    ser = serial.Serial(dev,9600) # Connect to Arduino's Serial
    print ("Connected to Arduino")
except:
    print ("Arduino not connected")

while True:
    light = input("Please choose a light. Green =1, Yellow =2, Red = 3\n") # input will be defined as an int
    if int(light) >7:
        break
    light = str(light)# turn int to string
    light = light.encode("utf-8") #turn string to byte
    ser.write(light)
    print(ser.readline())
     