import RPi.GPIO as GPIO
import smbus
import time
from subprocess import call

cmd_beg= 'espeak -ven+f3 -g1 -s150'
cmd_end= ' 2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file

#text = input("Enter the Text: ")
intro = "This is the Forget Me Not Child Safety System  A child has been left unattended in a vehicle and needs assistance."
car_description = "The child is in a " + " ' " + "black" + " ' " + "Nissan" + " ' " + "versa" + " ' "
GPS_Longitude = "at GPS Location " + " ' " + "30" + " ' " + " degrees " + " ' " + "North" + " ' "
GPS_Lattitude = " and" + " ' " + "50" + " ' " + " degrees " +  " ' " + "East" + " ' " 

print(intro + car_description + GPS_Longitude + GPS_Lattitude)

#Replacing ' ' with '_' to identify words in the text entered
intro = intro.replace(' ', '_')
car_description = car_description.replace(' ', '_')
GPS_Longitude = GPS_Longitude.replace(' ', '_')
GPS_Lattitude = GPS_Lattitude.replace(' ', '_')

time.sleep(1)
for num in range(0,1) :
    num=num+1
    #Calls the Espeak TTS Engine to read aloud a Text
    call([cmd_beg+cmd_out+intro+cmd_end], shell=True)
    call([cmd_beg+cmd_out+car_description+cmd_end], shell=True)
    call([cmd_beg+cmd_out+GPS_Longitude+cmd_end], shell=True)
    call([cmd_beg+cmd_out+GPS_Lattitude+cmd_end], shell=True)
    time.sleep(1)
