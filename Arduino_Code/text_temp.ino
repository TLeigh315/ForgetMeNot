
/**************************************************************************/
/*!
This is a demo for the Adafruit MCP9808 breakout
----> http://www.adafruit.com/products/1782
Adafruit invests time and resources providing this open source code,
please support Adafruit and open-source hardware by purchasing
products from Adafruit!
*/
/**************************************************************************/

#include <Wire.h>
#include "Adafruit_MCP9808.h"

#include <Adafruit_FONA.h>

#include <SoftwareSerial.h>
#include "Adafruit_FONA.h"

#define FONA_RX 3
#define FONA_TX 4
#define FONA_RST 2

char replybuffer[255];

SoftwareSerial fonaSS = SoftwareSerial(FONA_TX, FONA_RX);

Adafruit_FONA fona = Adafruit_FONA(FONA_RST);

uint8_t readline(char *buff, uint8_t maxbuff, uint16_t timeout = 0);

// Create the MCP9808 temperature sensor object
Adafruit_MCP9808 tempsensor = Adafruit_MCP9808();
int ledPin =8;
int max=74;

void setup() {
  Serial.begin(9600);
  Serial.println("MCP9808 demo");
  pinMode(ledPin, OUTPUT);
  // Make sure the sensor is found, you can also pass in a different i2c
  // address with tempsensor.begin(0x19) for example
  if (!tempsensor.begin()) {
    Serial.println("Couldn't find MCP9808!");
    while (1);
  }
  while (!Serial);
  Serial.println(F("FONA basic test"));
  Serial.println(F("Initializing....(May take 3 seconds)"));
  fonaSS.begin(4800); 
  if (! fona.begin(fonaSS)) {            
    Serial.println(F("Couldn't find FONA"));
    while (1);
  }
    Serial.println(F("FONA is OK"));

   char sendto[20], message[141];
   //int mynumber="8327978415";
   //char mymessage ="hey";
   flushSerial();
   Serial.print(F("Send to #"));
   readline(sendto, 20);
   Serial.println(sendto);
   Serial.print(F("Type out one-line message (140 char): "));
   //readline(message, 140);
   Serial.println(message);
   if (!fona.sendSMS(sendto, message)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
}

void loop() {
  //Serial.println("wake up MCP9808.... "); // wake up MSP9808 - power consumption ~200 mikro Ampere
  //tempsensor.wake();   // wake up, ready to read!

  // Read and print out the temperature, then convert to *F
  float c = tempsensor.readTempC();
  float f = c * 9.0 / 5.0 + 32;
  Serial.print("Temp: "); Serial.print(c); Serial.print("*C\t"); 
  Serial.print(f); Serial.println("*F");
  
  if (f>max) {
    Serial.println("Ayeeeee");
    digitalWrite(ledPin, HIGH);
  }

  if (f<max) {
    digitalWrite(ledPin, LOW);
  }
  
  //Serial.println("Shutdown MCP9808.... ");
  //tempsensor.shutdown(); // shutdown MSP9808 - power consumption ~0.1 mikro Ampere  
  delay(10000);
}

void flushSerial() {
    while (Serial.available()) 
    Serial.read();
}

uint8_t readline(char *buff, uint8_t maxbuff, uint16_t timeout) {
  uint16_t buffidx = 0;
  boolean timeoutvalid = true;
  if (timeout == 0) timeoutvalid = false;
  
  while (true) {
    if (buffidx > maxbuff) {
      break;
    }

    while(Serial.available()) {
      char c =  Serial.read();

      if (c == '\r') continue;
      if (c == 0xA) {
        if (buffidx == 0)   // the first 0x0A is ignored
          continue;
        
        timeout = 0;         // the second 0x0A is the end of the line
        timeoutvalid = true;
        break;
      }
      buff[buffidx] = c;
      buffidx++;
    }
    
    if (timeoutvalid && timeout == 0) {
      break;
    }
    delay(1);
  }
  buff[buffidx] = 0;  // null term
  return buffidx;
}
