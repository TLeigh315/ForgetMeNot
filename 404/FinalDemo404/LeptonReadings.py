#!/usr/bin/env python

import sys
import numpy as np
import cv2
from pylepton import Lepton
from time import sleep

def capture(flip_v = False, device = "/dev/spidev0.0"):
  with Lepton(device) as l:
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  #cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  #np.left_shift(a, 2, a)
  return np.int16(a)

if __name__ == '__main__':
    
    cal_slope = float(.0247)
    lepton_temp = float(30565/100)- int(273)
    #print('cal factor {0}'.format(cal_slope))
    rawvalues = np.zeros(50)
    sum = np.zeros(50)
    
    for x in range(50):
    
        image = capture()
        #copy = image.copy()
        #copy = cv2.GaussianBlur(copy, (3, 3), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(image)
        #(minVal1, maxVal1, minLoc1, maxLoc1) = cv2.minMaxLoc(copy)
        scaled =  (cal_slope * (maxVal - 8192)) + lepton_temp
        rawvalues[x] = scaled
        #print(sum)
        sleep(.01)
        #cv2.imwrite("IMAGE.png", image)
    
    else:
        averaged = np.mean(sum)
        anotherone = np.mean(rawvalues)
        print(" ")
        print('Average raw value {}'.format(anotherone))
        #print('Averaged {}'.format(averaged))
        print(" ")

