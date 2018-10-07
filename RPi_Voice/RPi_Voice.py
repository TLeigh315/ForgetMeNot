import pygame
#pygame.init()

#Intro= pygame.mixer.Sound("piano2.wav")
#Intro.play()

from subprocess import Popen, PIPE

pipes = dict(stdin=PIPE, stdout=PIPE, stderr=PIPE)
mplayer = Popen(["/home/pi/Desktop/404/RPi_Voice","Intro.m4a"], **pipes)

# to control u can use Popen.communicate
mplayer.communicate(input=b">")
sys.stdout.flush()