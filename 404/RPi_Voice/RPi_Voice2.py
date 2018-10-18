import pygame
from subprocess import call
import time

def RpiSays(words_to_speak):
    words_to_speak = str(words_to_speak)
    #Replacing ' ' with '_' to identify words in the text entered
    words_to_speak = words_to_speak.replace(' ', '_')

    cmd_beg= 'espeak -ven+f4 -g10 -s150'
    cmd_end= ' 2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
    cmd_out= '--stdout > /home/pi/Desktop/Text.wav ' # To store the voice file
    call([cmd_beg+cmd_out+words_to_speak+cmd_end], shell=True)

def militaryABC(letter):
    convert_letter = {
        "A" : "Alfa",
        "B" : "Bravo",
        "C" : "Charlie",
        "D" : "Delta",
        "E" : "Echo",
        "F" : "Foxtrot",
        "G" : "Golf",
        "H" : "Hotel",
        "I" : "India",
        "J" : "Juliett",
        "K" : "Kilo",
        "L" : "Lima",
        "M" : "Mike",
        "N" : "November",
        "O" : "Oscar",
        "P" : "Papa",
        "Q" : "Quebec",
        "R" : "Romeo",
        "S" : "Sierra",
        "T" : "Tango",
        "U" : "Uniform",
        "V" : "Victor",
        "W" : "Whiskey",
        "X" : "Xray",
        "Y" : "Yankee",
        "Z" : "Zulu",
        "1" : "One",
        "2" : "Two",
        "3" : "Three",
        "4" : "Four",
        "5" : "Five",
        "6" : "Six",
        "7" : "Seven",
        "8" : "Eight",
        "9" : "Nine",
        "0" : "Zero"
    }
    return convert_letter.get(letter, "Invalid Letter")
        
def EMScaller(car_color, car_type, car_license, Longitude, Latitude):
    pygame.mixer.init(frequency=48500, size=-16, channels = 2, buffer = 4096)
    pygame.init()
    pygame.mixer.init()
    Intro = pygame.mixer.Sound("Intro.wav")
    Car_Intro = pygame.mixer.Sound("Car_Description.wav")
    GPS_Intro = pygame.mixer.Sound("At_GPS_Location.wav")
    East = pygame.mixer.Sound("Degrees_East.wav")
    West = pygame.mixer.Sound("Degrees_West.wav")
    North = pygame.mixer.Sound("Degrees_North.wav")
    South = pygame.mixer.Sound("Degrees_South.wav")
    And = pygame.mixer.Sound("And.wav")
    License_Plate_Intro = pygame.mixer.Sound("License_Plate_Intro.wav")

    Intro.play()
    time.sleep(9)

    Car_Intro.play()
    time.sleep(3)

    RpiSays(car_color)
    RpiSays(car_type)

    License_Plate_Intro.play()
    time.sleep(2.5)
    for letter in car_license:
        RpiSays(militaryABC(letter))
        time.sleep(.5)

    GPS_Intro.play()
    time.sleep(3)
       

    if Longitude < 0:
        RpiSays(Longitude*-1)
        South.play()
    else:
        RpiSays(Longitude)
        North.play()
    time.sleep(1.5)

    And.play()
    time.sleep(2)

    if Latitude < 0:
        RpiSays(Latitude*-1)
        West.play()
    else:
        RpiSays(Latitude)
        East.play()
    time.sleep(2)

repeat = 2 #how many times voice call will run
talk_delay = 10 #how long to wait before beginning to talk

car_color = "black"
car_type = "Nissan Versa"
car_license = "LAC32YD"
Longitude = -33.354
Latitude = -56.244

EMScaller(car_color, car_type, car_license, Longitude, Latitude)
