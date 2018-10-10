#include <Wire.h>
#include "Adafruit_MCP9808.h"
#include <Adafruit_FONA.h>


#include <SoftwareSerial.h>
#include "Adafruit_FONA.h"

#define Arduino_RX 4
#define Arduino_TX 3
#define Reset 2

char replybuffer[255];

SoftwareSerial fonaSS = SoftwareSerial(Arduino_TX, Arduino_RX);

Adafruit_FONA fona = Adafruit_FONA(Reset);

uint8_t readline(char *buff, uint8_t maxbuff, uint16_t timeout = 0);

const int ledPin1 = 13;
const int ledPin2 = 9;
const int ledPin3 =8;

void setup() 
{
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  Serial.begin(9600); //determines data transfer rate. MUST be the same as baud rate in Rpi
  while (!Serial);
  Serial.println(F("FONA basic test"));
  Serial.println(F("Initializing....(May take 3 seconds)"));
  fonaSS.begin(4800); 
  if (! fona.begin(fonaSS)) {            
    Serial.println(F("Couldn't find FONA"));
    while (1);
  }
  Serial.println(F("FONA is OK"));
}

void loop() 
{
 if(Serial.available())
 { //check if data is coming in from Rpi
    SMS_type((Serial.read()-'0')); //function we use to pass on Serial.read() data
 }
 delay(500); //give it time to read data
}

void SMS_type(int n)
{
  //flushSerial(); //get rid of whatever number triggered SMS alert
  switch(n)
  {
    case 1:
    digitalWrite(ledPin1, HIGH);
    //HotCarAlert();
    delay(1000);
    digitalWrite(ledPin1,LOW);
    delay(1000);
    break;
    
    case 2:
    digitalWrite(ledPin2, HIGH);
    //TempRateAlert();
    delay(1000);
    digitalWrite(ledPin2,LOW);
    delay(1000);
    break;
    
    case 3:
    digitalWrite(ledPin3, HIGH);
    //WarningAlert();
    delay(1000);
    digitalWrite(ledPin3,LOW);
    delay(1000);
    break;

    case 4:
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, HIGH);
    //EMSWarningAlert();
    delay(1000);
    digitalWrite(ledPin1,LOW);
    digitalWrite(ledPin2,LOW);
    delay(1000);
    break;

    case 5:
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, HIGH);
    digitalWrite(ledPin3, HIGH);
    //EMScall();
    delay(1000);
    digitalWrite(ledPin1,LOW);
    digitalWrite(ledPin2,LOW);
    digitalWrite(ledPin3,LOW);
    delay(1000);
    break;

    case 6:
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin1, HIGH);
    //EMScallNotification();
    delay(1000);
    digitalWrite(ledPin3,LOW);
    digitalWrite(ledPin1,LOW);
    delay(1000);
    break;

    case 7:
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin2, HIGH);
    //ReedAlertSMS();
    delay(1000);
    digitalWrite(ledPin3,LOW);
    digitalWrite(ledPin2,LOW);
    delay(1000);
    break;    
  }
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

void HotCarAlert()
{
   flushSerial();// clear serial
   char primary_contact[21]="8327978415";
   char message[141] = "Your child has been left in the car. Return to your car immediately.";
   if (!fona.sendSMS(primary_contact,message)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
}

void TempRateAlert()
{
   flushSerial();// clear serial
   char primary_contact[21]="8327978415";
   char message[141] = "Your child has been left in the car and the temperature is rising rapidly. Return to your car immediately.";
   if (!fona.sendSMS(primary_contact,message)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
}

void WarningAlert()
{
   flushSerial();// clear serial
   char primary_contact[21]="8327978415";
   char message[141] = "Your child has been left in the car alone. Please return to your car immediately.";
   if (!fona.sendSMS(primary_contact,message)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
}

void EMSWarningAlert()
{
   flushSerial();// clear serial
   char primary_contact[21]="8327978415";
   char message[141] = "Your child has been left in the car alone. EMS will be contacted in 60 seconds. Please return to your car immediately.";
   if (!fona.sendSMS(primary_contact,message)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
}

void EMScall()
{
   flushSerial();// clear serial
   char primary_contact[21]="8327978415";
   if (!fona.callPhone(primary_contact)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
}

void EMScallNotification()
{
   flushSerial();// clear serial
   char primary_contact[21]="8327978415";
   char message[141] = "Your child has been left in the car alone for an extended period of time. EMS has been contacted. Please return to your car immediately.";
   if (!fona.sendSMS(primary_contact,message)) {
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
  uint16_t buffidx = 0; //set buffer index to 0
  boolean timeoutvalid = true;
  if (timeout == 0) timeoutvalid = false;
  
  while (true) {
    if (buffidx > maxbuff) { //make sure buffer index < character array
      break;
    }

    while(Serial.available()) { //check if there's data in serial and make sure they're the right characters
      char c =  Serial.read();

      if (c == '\r') continue; //ignore carraiage returns
      if (c == 0xA) {
        if (buffidx == 0)   // the first 0x0A is ignored
          continue;
        
        timeout = 0;         // the second 0x0A is the end of the line
        timeoutvalid = true;
        break;
      }
      buff[buffidx] = c; //add character to character array
      buffidx++; //iterate to go to potential add next character to character array
    }
    
    if (timeoutvalid && timeout == 0) { //if line has ended, stop reading line
      break;
    }
    delay(1);
  }
  buff[buffidx] = 0;  // null term replaces last term of array
  return buffidx;
}
