import pygame
import time
pygame.mixer.init(frequency=49000, size=-16, channels = 2, buffer = 4096)

Intro= pygame.mixer.Sound("piano2.wav")
Intro.play()
time.sleep(4)

Me = pygame.mixer.Sound("Intro.wav")
Me.play()
#pygame.event.wait()

