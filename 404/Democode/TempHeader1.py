import RPi.GPIO as GPIO
import smbus
import time
import serial
from subprocess import call
from LIS3DH import LIS3DH

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
MCP9808_DEFAULT_ADDRESS			= 0x18

# MCP9808 Register Pointer
MCP9808_REG_CONFIG				= 0x01 # Configuration Register
MCP9808_REG_UPPER_TEMP			= 0x02 # Alert Temperature Upper Boundary Trip register
MCP9808_REG_LOWER_TEMP			= 0x03 # Alert Temperature Lower Boundary Trip register
MCP9808_REG_CRIT_TEMP			= 0x04 # Critical Temperature Trip register
MCP9808_REG_AMBIENT_TEMP		= 0x05 # Temperature register
MCP9808_REG_MANUF_ID			= 0x06 # Manufacturer ID register
MCP9808_REG_DEVICE_ID			= 0x07 # Device ID/Revision register
MCP9808_REG_RSLTN				= 0x08 # Resolution register

# Configuration register values
MCP9808_REG_CONFIG_DEFAULT		= 0x0000 # Continuous conversion (power-up default)
MCP9808_REG_CONFIG_SHUTDOWN		= 0x0100 # Shutdown
MCP9808_REG_CONFIG_CRITLOCKED	= 0x0080 # Locked, TCRIT register can not be written
MCP9808_REG_CONFIG_WINLOCKED	= 0x0040 # Locked, TUPPER and TLOWER registers can not be written
MCP9808_REG_CONFIG_INTCLR		= 0x0020 # Clear interrupt output
MCP9808_REG_CONFIG_ALERTSTAT	= 0x0010 # Alert output is asserted
MCP9808_REG_CONFIG_ALERTCTRL	= 0x0008 # Alert Output Control bit is enabled
MCP9808_REG_CONFIG_ALERTSEL		= 0x0004 # TA > TCRIT only
MCP9808_REG_CONFIG_ALERTPOL		= 0x0002 # Alert Output Polarity bit active-high
MCP9808_REG_CONFIG_ALERTMODE	= 0x0001 # Interrupt output

# Resolution Register Value
MCP9808_REG_RSLTN_5			= 0x00 # +0.5C
MCP9808_REG_RSLTN_25			= 0x01 # +0.25C
MCP9808_REG_RSLTN_125			= 0x02 # +0.125C
MCP9808_REG_RSLTN_0625			= 0x03 # +0.0625C

class alert():
    
    def GSMstartup(self):
        # Enable Serial Communication
        print("Begin SMS procedure")
        port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1) #Declare what serial port to use

        #Flush Serial
        port.flushInput()
        time.sleep(.5)
        port.flushOutput()
        time.sleep(.5)
        
    # Transmitting AT Commands to the Modem
    def GSMconvo(self, message):
        port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1) #Declare what serial port to use
        GSMreset = 12
        GPIO.setup(GSMreset,GPIO.OUT)
        GPIO.setup(GSMpower,GPIO.OUT)
        GPIO.output(GSMpower,1) #Turn on GSM
        
        sendGSM = message + '\r' #Change original message into GSM message format
        print(sendGSM.encode('utf-8')) #encode message and print to terminal
        port.write(sendGSM.encode('utf-8')) #encode message and send to serial port
        port.readline() #This WILL be '\r\n'. Need line to read GSM response on next line
        rcv=port.readline()
        print (rcv) #Read and print GSM response to terminal
        
        if rcv == "ERROR\r\n" & message !="AT+CMGF=1\r":
            GPIO.output(GSMreset,0) #Reset GSM
            timepassed = 0
            
            while True:
                
                
                
                time.sleep(1)
                timepassed = timepassed + 1 #Keep track of how long Command has tried to send
                
                if timepassed > 15:
                    print("Too much time has passed for GSM Command!") #Temporary
                    time.sleep(5) #Temporary
                
            
            
            
        time.sleep(.5)
    
    def GSMsms (self, textnumber, textmessage):
        alert.GSMconvo(self,'AT')
        alert.GSMconvo(self,'ATE0') # Disable the Echo
        alert.GSMconvo(self,'ATE0') # Disable the Echo
        alert.GSMconvo(self,'AT+CVHU=0')
        alert.GSMconvo(self,'ATI')
        alert.GSMconvo(self,'AT+GMM')
        alert.GSMconvo(self,'AT+CPMS="SM","SM",SM"')
        alert.GSMconvo(self,'AT+CSCS="GSM"')
        alert.GSMconvo(self,'AT+CMGF=1') # Select Message format as Text mode 
        alert.GSMconvo(self,'AT+CNMI=2,1,0,0,0') # New SMS Message Indications
        alert.GSMconvo(self,'AT+CMGS="1'+ textnumber +'"') # Determine what number to text
        alert.GSMconvo(self,textmessage) #Determine content of text
        alert.GSMconvo(self,"\x1A") # Enable to send SMS

    def danger_temp_alert(self, textnumber):
        alert.GSMstartup(self)
        message = "Car has exceeded max temperature!"
        print(message)
        alert.GSMsms(self,textnumber,message)
            #if reset = 1 alert.GSMsms(self,textnumber,message)
        
    def temp_rate_alert(self, textnumber):
        alert.GSMstartup(self)
        message = "Car temperature is increasing dangerously fast!"
        print(message)
        alert.GSMsms(self,textnumber,message)
        
    def warning_alert(self, textnumber):
        alert.GSMstartup(self)
        message = "Child has been left in car alone!"
        print(message)
        alert.GSMsms(self,textnumber,message)
    
    def EMS_warning_alert(self, textnumber):
        alert.GSMstartup(self)
        message = "Your child has been left alone in a car after several alerts. Please return to your car. EMS will be contacted in 60 seconds."
        print(message)
        alert.GSMsms(self,textnumber,message)
        
    def EMS_call(self,textnumber):
        alert.GSMstartup(self)
        message = "Calling EMS"
        print(message)
        alert.GSMsms(self,textnumber,message)
        
    def parent_EMS_not(self,textnumber):
        alert.GSMstartup(self)
        message = "EMS has been contacted"
        print(message)
        alert.GSMsms(self,textnumber,message)

    def seat_belt_alert(self, textnumber):
        alert.GSMstartup(self)
        message = "Child is unbuckled in a moving car!"
        print(message)
        alert.GSMsms(self,textnumber,message)
        
class temp_sensor():

    def readTempF(self):
        data = bus.read_i2c_block_data(MCP9808_DEFAULT_ADDRESS, MCP9808_REG_AMBIENT_TEMP, 2)
		
	# Convert the data to 13-bits
        TempC = ((data[0] & 0x1F) * 256) + data[1]
        if TempC > 4095 :
            TempC -= 8192
        TempC = TempC * 0.0625
        TempF = TempC * 1.8 + 32
        return TempF
    
    def calc_rate(self, temp, base_temp, base_time, timer, start):
        
        if start== 0: #check if program just started
            start = 1
            last_temp = temp #ignore initial last_temp value
            base_temp = temp #set base temp. Will be updated every minute
            base_time = timer
            #print("calc rate base_temp : " + str(base_temp))
            #print("calc rate base_time : " + str(base_time))
            #print("New last_temp value: " + str(last_temp))
               
        temp_rate = temp - base_temp # calculate how fast temperature has changed in last minute
        #print("Base temperature was " + str(base_temp) + " at the " + str(base_time) + " second mark.")
        print("Temperature change within the last minute : " + str(temp_rate))
        
        if (timer-base_time) > 59 : #Check if minute has passed
            base_time=timer #update base time every minute
            base_temp=temp #update base temp every minute
            
        return {"temp_rate" : temp_rate, "base_temp" : base_temp, "base_time" : base_time, "start" :start}

    def Temperature(self, base_temp, base_time, timer, start, danger_rate, last_alert, first_alert, serial, max):

        print("\r\nCurrent time is: " +str(timer))
        print("First temperature alert time: " +str(first_alert))
        print("Last temperature alert time: " + str(last_alert))

        temp_rate_bit = 0
        danger_temp_bit = 0
        temp = temp_sensor.readTempF(self) #Read temperature in F

        #print ("Max temperature : " + str(max))
        print ("Current Temperature in Fahrenheit : %.2f F"%(temp)) #Display temperature
        
        if str(temp) > str(max): #check if current temp is higher than defined max temp
            print("Dangerously hot temperatures!")
            if last_alert == 0 :
                last_alert=timer
                danger_temp_bit = 1 #trigger danger_temp_alert() SMS warning
                
            if (timer-last_alert) > 60 : #If it's been more than a minute since the last alert send another
                last_alert=timer
                danger_temp_bit = 1 #trigger danger_temp_alert() SMS warning

        rate = temp_sensor.calc_rate(self, temp, base_temp, base_time, timer, start) #Calculate change in temperature
        start = rate['start']
        base_time = rate['base_time']
        base_temp = rate['base_temp']
    
        if rate['temp_rate'] > danger_rate : #Check if temperature is rising too quickly
            #print("Dangerous increase in temperature!")
        
            if last_alert == 0 :
                last_alert=timer
                temp_rate_bit = 1 #trigger temp_rate_alert() SMS warning
                
            if (timer-last_alert) > 60 : #If it's been more than a minute since the last alert send another
                last_alert=timer
                temp_rate_bit = 1 #trigger temp_rate_alert() SMS warning
        
        return {"base_temp" : base_temp, "base_time" : base_time, "start" : start, "last_alert" : last_alert, "temp_rate_bit" : temp_rate_bit, "danger_temp_bit" : danger_temp_bit}
        
class accelerometer_sensor() :

    def rateAccel(self, movingcar, currentx, currenty, currentz, lastx, lasty, lastz):
        differencex = currentx - lastx
        differencey = currenty - lasty
        differencez = currentz - lastz
        #print("\rdiffX: %.6f\tdiffY: %.6f\tdiffZ: %.6f \t m/s^2" % (differencex, differencey, differencez))

        if (abs(differencex)>movingcar) | (abs(differencey)>movingcar) | (abs(differencez)>movingcar) :
            print("You're moving!")
            return 1

        else :
            print("Car isn't moving.")
            return 0

    def Accelerometer_sensor(self, serial, timer, reed_input, movingcar, last_alert, start_program, lastx, lasty, lastz):
        Accelerometer = LIS3DH()
        reed_bit = 0

        x = Accelerometer.getX()
        y = Accelerometer.getY()
        z = Accelerometer.getZ()
        
        if start_program == 0 : #prevents false acceleration alerts
            i = 0
            start_program = 1
            lastx = x
            lasty = y
            lastz = z
            #print("\rnewlastX: %.6f\tnewlastY: %.6f\tnewlastZ: %.6f \t m/s^2" % (x, y, z))
    
        #  Display results (acceleration is measured in m/s^2)
        print("\rX: %.6f\tY: %.6f\tZ: %.6f \td m/s^2" % (x, y, z))
        #print("\rlastX: %.6f\tlastY: %.6f\tlastZ: %.6f \t m/s^2" % (lastx, lasty, lastz))

        if reed_input == 1 : #check if child is buckled
            print("Seat belt buckled")
        else :
            print("Seat unbuckled")
                
        if accelerometer_sensor.rateAccel(self, movingcar, x, y, z, lastx, lasty, lastz) == 1 : #if car is moving
            if reed_input == 0 : #if seat is unbuckled update last_alert
                if last_alert == 0 : #If parent hasn't been notified
                    last_alert = timer #Update last_alert time
                    reed_bit = 1 #trigger danger_temp_alert() SMS warning
                    
                if (timer-last_alert) > 60*5 : #If it's been more than 5 minutes since the last alert send another
                    last_alert = timer #Update last_alert time
                    reed_bit = 1 #trigger danger_temp_alert() SMS warning
            
                #start_program = 0 #reset program values
                

        #Update coordinate values
        lastx = x
        lasty = y
        lastz = z
        

        return {"reed_bit" : reed_bit, "last_alert" : last_alert, "start_program" : start_program, "lastx" : lastx, "lasty" : lasty, "lastz" : lastz}

