import RPi.GPIO as GPIO
import smbus
import time
import serial
from subprocess import call

# Enable Serial Communication with GSM
port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1) #Declare what serial port to use

# Define/Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GSMreset = 12
GPIO.setup(GSMreset,GPIO.OUT)
       
class alert():
    def FlushSerial(self):
        #Flush Serial
        port.flushInput()
        time.sleep(.5)
        port.flushOutput()
        time.sleep(.5)

    def GSMconvo(self, message):
        sendGSM = message + '\r' #Change original message into GSM message format
        print(sendGSM.encode('utf-8')) #encode message and print to terminal
        port.write(sendGSM.encode('utf-8')) #encode message and send to serial port
        port.readline() #This WILL be '\r\n'. Need line to read GSM response on next line
        rcv=port.readline()
        print (rcv) #Read and print GSM response to terminal
        time.sleep(.5)
        if rcv == "ERROR\r\n": raise ValueError("Returning to the GSM function")
      
    def GSMsms (self, textnumber, textmessage):
        try:
            # Transmitting AT Commands to the Modem
            alert.GSMconvo(self,'AT')
            alert.GSMconvo(self,'ATE0') # Disable the Echo
            alert.GSMconvo(self,'ATE0') # Disable the Echo
            alert.GSMconvo(self,'AT+CVHU=0')
            alert.GSMconvo(self,'ATI')
            alert.GSMconvo(self,'AT+GMM')
            alert.GSMconvo(self,'AT+CPMS="SM","SM","SM"')
            alert.GSMconvo(self,'AT+CSCS="GSM"')
            alert.GSMconvo(self,'AT+CMGF=1') # Select Message format as Text mode 
            alert.GSMconvo(self,'AT+CNMI=2,1,0,0,0') # New SMS Message Indications
            alert.GSMconvo(self,'AT+CMGS="1'+ textnumber +'"') # Determine what number to text
            alert.GSMconvo(self,textmessage) #Determine content of text
            alert.GSMconvo(self,"\x1A") # Enable to send SMS
            return 1 #Let us know if SMS text was successfull

        except ValueError as err:
            return 0 #Let us know if SMS text failed

    def GSMcall (self, callnumber):
        try:
            # Transmitting AT Commands to the Modem
            alert.GSMconvo(self,'AT')
            alert.GSMconvo(self,'ATE0') # Disable the Echo
            alert.GSMconvo(self,'ATE0') # Disable the Echo
            alert.GSMconvo(self,'AT+CVHU=0')
            alert.GSMconvo(self,'ATI')
            alert.GSMconvo(self,'AT+GMM')
            alert.GSMconvo(self,'AT+CPMS="SM","SM","SM"')
            #alert.GSMconvo(self,'AT+CPMS=COPS?')
            alert.GSMconvo(self,'ATZ')
            alert.GSMconvo(self,'AT+CUSD=1') #Allows control of the Unstructered Supplementary Service Data
            alert.GSMconvo(self,'ATD+1' + callnumber + ';') # Determine what number to call
            while True:
                rcv=port.readline()
                print(rcv)
                if ( rcv == "NO CARRIER\r\n"):
                    break #Hang up if recipent hangs up
             
            return 1 #Let us know if call was successfull

        except ValueError as err:
            return 0 #Let us know if call failed     
        
    def GSMerrorfunc(self, GSMerror):
        GPIO.output(GSMreset,1) #Reset GSM
        GPIO.output(GSMreset,0) #Turn on GSM
        GSMerror = GSMerror + 1 #Keep track of how many times GSM has thrown error
        if GSMerror >= 3:
            raise StopIteration("Too many GSM errors. Quit trying to use GSM")

        print("GSM has thrown " + str(GSMerror) + " error(s) \n\n\n")
        alert.FlushSerial(self)
        time.sleep(5) #Allow time for GSM to power back on
        return GSMerror #Send updated GSM error count to other functions

    def StayorGoSMS(self,textnumber,message):
        alert.FlushSerial(self)
        GSMerror = 0 # Keeps track of how many times GSM has thrown an error
        success = alert.GSMsms(self,textnumber,message) #Send SMS Text and let us know if attempt was succesfull
        while True:
            if  success == 1:
                print("SMS successful. Total GSM errors: " + str(GSMerror))
                return GSMerror #Send updated GSM error count to Main function
                break #If Message was sent successully, continue with Main Code
            else:
                alert.FlushSerial(self)
                GSMerror = alert.GSMerrorfunc(self, GSMerror) #Update the GSMerror count
                success = alert.GSMsms(self,textnumber,message) #Resend text
         
    def seat_belt_alert(self, textnumber):
        message = "Child is unbuckled in a moving car!"
        alert.StayorGoSMS(self,textnumber,message)

    def warning_alert(self, textnumber):
        message = "Child has been left in car alone!"
        alert.StayorGoSMS(self,textnumber,message)
    
    def danger_temp_alert(self, textnumber):
        message = "Car has exceeded max temperature!"
        alert.StayorGoSMS(self,textnumber,message)
        
    def temp_rate_alert(self, textnumber):
        message = "Car temperature is increasing dangerously fast!"
        alert.StayorGoSMS(self,textnumber,message)
        
    def EMS_warning_alert(self, textnumber):
        message = "Your child has been left alone in a car after several alerts. Please return to your car. EMS will be contacted in 60 seconds."
        alert.StayorGoSMS(self,textnumber,message)
        
    def parent_EMS_not(self,textnumber):
        message = "EMS has been contacted"
        alert.StayorGoSMS(self,textnumber,message)
  
    def EMS_call(self,callnumber):
        alert.FlushSerial(self)
        GSMerror = 0 # Keeps track of how many times GSM has thrown an error
        success = alert.GSMcall(self,callnumber) #Send SMS Text and let us know if attempt was succesfull
        while True:
            if  success == 1:
                print("SMS successful. Total GSM errors: " + str(GSMerror))
                return GSMerror #Send updated GSM error count to Main function
                break #If Message was sent successully, continue with Main Code
            else:
                alert.FlushSerial(self)
                GSMerror = alert.GSMerrorfunc(self, GSMerror) #Update the GSMerror count
                success = alert.GSMcall(self,callnumber) #Resend text
  
