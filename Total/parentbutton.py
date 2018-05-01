import RPi.GPIO as GPIO
import time
import TempHeader1
import serial
import subprocess

dev = subprocess.check_output('ls /dev/ttyACM*', shell=True) #find out what name the Arduino is under
print (dev) #display Arduino name (will be shown in bytes)
dev=dev.decode("utf-8") #convert Arduino name from bytes to string
dev=dev.replace("\n","") #get rid of \n

try:
    ser = serial.Serial(dev,9600) # Connect to Arduino's Serial
    print ("Connected to Arduino")
except:
    print ("Arduino not connected")

###########################################################################################
tempsensor = TempHeader1.temp_sensor()#Create MCP9808 temp sensor object
alert = TempHeader1.alert() #Create alert object
###########################################################################################

###########################################################################################
start_time = 0 #TEMPORARY
timer = start_time #inital timer value. Timer will be in seconds
last_alert = 0 #time since last alert
danger_rate = 10
last_temp = 0 # keep track of last temp measurement
base_temp = 0
base_time = 0
temp_rate = 0 #difference between current and last temperature
start = 0 #will be zero only for timer = 1
BLEonbutton = 40 #onbutton represents parent leaving BLE range
BLEoffbutton= 38 #offbutton represents parent returning to BLE Range
Acconbutton = 35  
Accoffbutton = 33 
timer_speed = 1 #timer iterates once/second
max = 76 #maximum temperature
first_alert= 0 #time of first alert
over = 0 # will allow program to end when EMS is called
i = 0
#########################################################################################

###################################################################
repeat = 5 #how many times voice call will run
talk_delay = 10 #how long to wait before beginning to talk
car_color = "black"
car_make = "Nissan"
car_model = "Versa"
Longitude = 33.354
Long_Dir = "North"
Lattitude = 56.244
Latt_Dir = "East"
###################################################################
print("Current Temperature is: %.2f F" %tempsensor.readTempF())      
print("Maximum car temperature is: " + str(max))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BLEonbutton,GPIO.IN, GPIO.PUD_DOWN) 
GPIO.setup(BLEoffbutton,GPIO.IN, GPIO.PUD_DOWN) 
GPIO.setup(Acconbutton,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(Accoffbutton,GPIO.IN, GPIO.PUD_DOWN)

print("Press BLEonbutton to symbolize parent's leaving child in car.")

while True:
    if (GPIO.input(BLEonbutton) == 1 ) & ( GPIO.input(BLEoffbutton) == 0 ): #if ONLY the onbutton is pushed
        print("OnButton Pressed")
        
        alert.warning_alert(ser) #send first warning text
        print("Time in seconds "+str(timer) + "\n")
        
        while (GPIO.input(BLEoffbutton) == 0) :# offbutton isn't pushed (parent hasn't returned)
            #calculate temperature alert parameters
            print("first alert was given at : " + str(first_alert))
            print("last alert was given at : " + str(last_alert))
            temperature = tempsensor.Temperature(base_temp, base_time, timer, start, danger_rate, last_alert, ser, max)
            
            if (temperature['danger_temp_bit']) == 1 | (temperature['temp_rate_bit']) == 1 : #keep track of when first alert was made
                i = i + 1
                print("iteration : " +str(i))
                print("last alert was given at : " + str(last_alert))
                if i == 1 : #only save first alert once
                    first_alert = temperature['last_alert']
                    
            if (timer-first_alert) == 4*60 : #if it's been 4 min since first temp alert call EMS
                alert.parent_EMS_not(ser)
                alert.EMS_call(ser)
                TempHeader1.EMS_caller(repeat, talk_delay, car_color, car_make, car_model, Longitude, Long_Dir, Lattitude, Latt_Dir)
                over = 1
                
            if temperature['danger_temp_bit'] == 1:
                alert.danger_temp_alert(ser)
                
            if temperature['temp_rate_bit'] == 1 :
                alert.temp_rate_alert(ser)
                
            if (timer == 60*5) : #if child has been left in car for 5 min send warning text
                alert.warning_alert(ser)
            
            if (timer == 60*9) : #if child has been left in car for 9 min, tell parents that EMS is about to be contacted
                alert.EMS_warning_alert(ser)
            
            if (timer == 60*10) : #if child has ben left in car for 10 min , tell parents that EMS has been contacted and call EMS
                alert.parent_EMS_not(ser)
                alert.EMS_call(ser)
                TempHeader1.EMS_caller(repeat, talk_delay, car_color, car_make, car_model, Longitude, Long_Dir, Lattitude, Latt_Dir)
                over = 1
                break
            
            time.sleep(timer_speed) # wait for ___ seconds
            
            #Update values
            base_temp = temperature['base_temp']
            base_time = temperature['base_time']
            start = temperature['start']
            last_alert = temperature['last_alert']
            timer = timer + 1
            
            print("Time in seconds "+str(timer) + "\n")
            
            if GPIO.input(BLEoffbutton) == 1 : # If offbutton is pushed (parent returns within BLE range)
                print("BLEoffbutton Pressed")
                timer = start_time #start timer over
                break
            
        if over == 1 :
            break
            
            
        
    