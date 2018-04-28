import time

from Adafruit_MCP9808.MCP9808 import MCP9808 as tempsensor
#empsensor = MCP9808

while True:
	temp = tempsensor.readTempF()
	print ("Temperature in Fahrenheit : ",temp)
	time.sleep(1)

