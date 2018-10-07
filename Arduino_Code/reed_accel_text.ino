////////////////////Read Sensor Variables
const int reed = 2;  //Pin Reed
const int pinLed    = 7;  //Pin LED
int switchState = 0;
int update_time=1000; //check reed sensor every second
//////////////////////////////////////////////////////////

/////////////////////Accelerometer Sensor Variables
float movingcar=1; //car's accerlation in m/s^s
float lastx; //last known X Coordinates
float lasty; //last known Y Coordinates
float lastz; //last known Z Coordinates
float differencex; //difference between current and last known X Coordinates
float differencey; //difference between current and last known Y Coordinates
float differencez; //difference between current and last known Z Coordinates
//////////////////////////////////////////////////////////

//////////////SMS definitions/headers
#include <SoftwareSerial.h>
#include "Team7GSM.h"

#define FONA_RX 3
#define FONA_TX 4
#define FONA_RST 2
/////////////////////////////////////////////////

///////////////SMS Variables/functions
char replybuffer[255];
SoftwareSerial fonaSS = SoftwareSerial(FONA_TX, FONA_RX);
Adafruit_FONA fona = Adafruit_FONA(FONA_RST);
uint8_t readline(char *buff, uint8_t maxbuff, uint16_t timeout = 0);
/////////////////////////////////////////////////

/////////////////////Accelerometer Sensor Definitions and headers
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

Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS, LIS3DH_MOSI, LIS3DH_MISO, LIS3DH_CLK);

#if defined(ARDUINO_ARCH_SAMD)
#endif

/*
 * Wiring
 * Vin>>>>>>>>>5V
 * GND>>>>>>>>>GND
 * SCL>>>>>>>>>13
 * SDA>>>>>>>>>11
 * SD0>>>>>>>>>12
 * CS>>>>>>>>>>10
 */
 
//////////////////////////////////////////////////////////

void setup(void) {
  getReadySMS();
  getReadyAccel();
  pinMode(pinLed, OUTPUT); //LED is OUTPUT
  pinMode(reed, INPUT); //Reed Sensor is INPUT
}

void loop(){
  Accel();
}

void Accel() {
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

  if(lastx==0 && lasty==0 && lastz==0){ //ignore first round of old values because they have no data
    lastx= event.acceleration.x;
    lasty= event.acceleration.y;
    lastz= event.acceleration.z;
    Serial.print("newlastX: "); Serial.print(lastx);
    Serial.print("\t\tnewlastY: "); Serial.print(lasty); 
    Serial.print("\t\tnewlastZ: "); Serial.print(lastz); 
    Serial.print(" m/s^2 \n");
  }
  
  rateAccel(event.acceleration.x,event.acceleration.y,event.acceleration.z);
  StationarycheckReed();//won't use for final
  
  /* Update coordingate values*/
  lastx= event.acceleration.x;
  lasty= event.acceleration.y;
  lastz= event.acceleration.z;

  delay(1000); 
  
}

int rateAccel(float currentx, float currenty, float currentz){
  differencex = currentx - lastx;
  differencey = currenty - lasty;
  differencez = currentz - lastz; 


  Serial.print("differenceX: "); Serial.print(differencex);
  Serial.print("\tdifferenceY: "); Serial.print(differencey); 
  Serial.print("\tdifferenceZ: "); Serial.print(differencez); 
  Serial.println(" m/s^2");
  
  if (abs(differencex)>movingcar || abs(differencey)>movingcar || abs(differencez>movingcar)){
    Serial.println("You're moving!");
    MovingcheckReed();
    /*Reset old coordinates to prevent false alarms when process starts over*/
    lastx=0;
    lasty=0;
    lastz=0;
  }
}

void StationarycheckReed(){//not necessary for final
  switchState = digitalRead(reed);  //Leggo il valore del Reed
  if (switchState == HIGH)
  {
    digitalWrite(pinLed, HIGH);
    Serial.println("Seat is buckled\n");
  }
  else
  {
    digitalWrite(pinLed, LOW);
    Serial.println("Seat is unbuckled\n");
  }
}

void MovingcheckReed(){
  switchState = digitalRead(reed);  
  if (switchState == HIGH)
  {
    digitalWrite(pinLed, HIGH);
    Serial.println("Seat is buckled");
  }
  else
  {
    digitalWrite(pinLed, LOW);
    Serial.println("Seat is unbuckled");
    ReedAlertSMS();
    while (switchState == LOW){
      switchState = digitalRead(reed); 
      Serial.println("Still not buckled"); 
      delay(1000);
    }
  }
}

void getReadyAccel(){
  Serial.begin(115200);
  Serial.println("LIS3DH test");
  
  if (! lis.begin(0x18)) {   // change this to 0x19 for alternative i2c address
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("LIS3DH found!");
  
  lis.setRange(LIS3DH_RANGE_4_G);   // 2, 4, 8 or 16 G!
  
  Serial.print("Range = "); Serial.print(2 << lis.getRange());  
  Serial.println("G");
}

void getReadySMS(){
  while (!Serial);
  Serial.begin(115200);
  Serial.println(F("FONA basic test"));
  Serial.println(F("Initializing....(May take 3 seconds)"));
  fonaSS.begin(4800); 
  if (! fona.begin(fonaSS)) {            
    Serial.println(F("Couldn't find FONA"));
    while (1);
  }
  Serial.println(F("FONA is OK"));
}

void ReedAlertSMS() {
   char sendto[21]="8327978415";
   char message[141]="Vehicle movemnet has been detected. You're child is not buckled correctly.";
   flushSerial();
   Serial.print(F("Send to #:"));
   Serial.println(sendto);
   Serial.print(F("Type out one-line message (140 char): "));
   Serial.println(message);
   if (!fona.sendSMS(sendto, message)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
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
