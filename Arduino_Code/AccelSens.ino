// Basic demo for accelerometer readings from Adafruit LIS3DH

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>

// Used for software SPI
#define LIS3DH_CLK 13
#define LIS3DH_MISO 12
#define LIS3DH_MOSI 11
// Used for hardware & software SPI
#define LIS3DH_CS 10
/*
 * Wiring
 * Vin>>>>>>>>>5V
 * GND>>>>>>>>>GND
 * SCL>>>>>>>>>13
 * SDA>>>>>>>>>11
 * SD0>>>>>>>>>12
 * CS>>>>>>>>>>10
 */
// software SPI
Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS, LIS3DH_MOSI, LIS3DH_MISO, LIS3DH_CLK);

#if defined(ARDUINO_ARCH_SAMD)
#endif

float lastx;
float lasty;
float lastz;
float differencex;
float differencey;
float differencez;

void setup(void) {
#ifndef ESP8266
  while (!Serial);     // will pause Zero, Leonardo, etc until serial console opens
#endif

  Serial.begin(115200);
  Serial.println("LIS3DH test!");
  
  if (! lis.begin(0x18)) {   // change this to 0x19 for alternative i2c address
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("LIS3DH found!");
  
  lis.setRange(LIS3DH_RANGE_4_G);   // 2, 4, 8 or 16 G!
  
  Serial.print("Range = "); Serial.print(2 << lis.getRange());  
  Serial.println("G");
}

void loop() {
  lis.read();      // get X Y and Z data at once
  sensors_event_t event; 
  lis.getEvent(&event);
  
  /* Display the results (acceleration is measured in m/s^2) */
  Serial.print("X: "); Serial.print(event.acceleration.x);
  Serial.print("\t\t\tY: "); Serial.print(event.acceleration.y); 
  Serial.print("\t\tZ: "); Serial.print(event.acceleration.z); 
  Serial.print(" m/s^2 \n");
 
  Serial.print("lastX: "); Serial.print(lastx);
  Serial.print("\t\tlastY: "); Serial.print(lasty); 
  Serial.print("\t\tlastZ: "); Serial.print(lastz); 
  Serial.print(" m/s^2 \n");
  
  differencex = event.acceleration.x - lastx;
  differencey = event.acceleration.y - lasty;
  differencez = event.acceleration.z - lastz; 
  
  Serial.print("differenceX: "); Serial.print(differencex);
  Serial.print("\tdifferenceY: "); Serial.print(differencey); 
  Serial.print("\tdifferenceZ: "); Serial.print(differencez); 
  Serial.println(" m/s^2 \n");
  
  lastx= event.acceleration.x;
  lasty= event.acceleration.y;
  lastz= event.acceleration.z;

  
  delay(1000); 
  
}
