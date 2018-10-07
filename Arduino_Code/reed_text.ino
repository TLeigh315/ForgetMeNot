/////////////////////Read Sensor Variables
const int reed = 2;  //Pin Reed
const int pinLed    = 7;  //Pin LED
int switchState = 0;
int update_time=1000; //check reed sensor every second
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

void setup()
{
  getReadySMS();
  pinMode(pinLed, OUTPUT); //LED is OUTPUT
  pinMode(reed, INPUT); //Reed Sensor is INPUT
}
void loop()
{
  delay(1000);
  switchState = digitalRead(reed);  //Leggo il valore del Reed
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
