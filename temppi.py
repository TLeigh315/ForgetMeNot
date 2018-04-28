import smbus
import time
bus = smbus.SMBus(1)
config = [0x00, 0x00]
bus.write_i2c_block_data(0x18, 0x01, config)

bus.write_byte_data(0x18, 0x08, 0x03)

time.sleep(.5)

data=bus.read_i2c_block_data(0x18, 0x05, 2)

ctemp = ((data[0] & 0x1F) * 256) +data[1]
print (ctemp)
if ctemp > 4095 :
    ctemp -= 8192
print (ctemp)
ctemp = ctemp / 16
print(ctemp)
ftemp = ctemp * 1.8 + 32
print(ftemp)

print("Temperature in Fahrenheit : ",ftemp)