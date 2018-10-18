import time
from subprocess import call
repeat = 2 #how many times voice call will run
talk_delay = 10 #how long to wait before beginning to talk
car_color = "black"
car_make = "Nissan Versa"
car_model = "Versa"

Longitude = -33.354
if Longitude < 0:
    Longitude = Longitude *-1
    Long_Dir = "South"
else:
    Long_Dir = "North"

Latitude = 56.244
if Latitude < 0:
    Latitude = Latitude *-1
    Lat_Dir = "West"
else:
    Lat_Dir = "East"


cmd_beg= 'espeak -ven+f3 -g1 -s150'
cmd_end= ' 2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file

#text = input("Enter the Text: ")
intro = "This is the Forget Me Not Child Safety System  A child has been left unattended in a vehicle and needs assistance."
car_description = "The child is in a " + " ' " + str(car_color) + " ' " + " ' " + str(car_make) + " ' "
GPS_Longitude = " at GPS Location " + " ' " + str(Longitude) + " ' " + " degrees " + " ' " + str(Long_Dir) + " ' "
GPS_Latitude = " and" + " ' " + str(Latitude) + " ' " + " degrees " +  " ' " + str(Lat_Dir) + " ' " 

print(intro + car_description + GPS_Longitude + GPS_Latitude)

#Replacing ' ' with '_' to identify words in the text entered
intro = intro.replace(' ', '_')
car_description = car_description.replace(' ', '_')
GPS_Longitude = GPS_Longitude.replace(' ', '_')
GPS_Latitude = GPS_Latitude.replace(' ', '_')

time.sleep(1)
for num in range(0,repeat) :
    num=num+1
    #Calls the Espeak TTS Engine to read aloud a Text
    call([cmd_beg+cmd_out+intro+cmd_end], shell=True)
    call([cmd_beg+cmd_out+car_description+cmd_end], shell=True)
    call([cmd_beg+cmd_out+GPS_Longitude+cmd_end], shell=True)
    call([cmd_beg+cmd_out+GPS_Latitude+cmd_end], shell=True)
    time.sleep(1)
