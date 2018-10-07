//////////////Temperature definitions/headers
#include <Wire.h>
#include "AmbientTemperatureSensor.h"
/*
 * SCL>>>>A5
 * SDA>>>>A4
 * VDD>>>>5V
 * GND>>>>GND
 */
/////////////////////////////////////////////////

//////////////SMS definitions/headers
#include <SoftwareSerial.h>
#include "Team7GSM.h"

#define FONA_RX 3
#define FONA_TX 4
#define FONA_RST 2
/////////////////////////////////////////////////

//////////////////Temperature Variables/functions
AmbientTemperatureSensor tempsensor = AmbientTemperatureSensor();
int max=76;
float danger=1.9;
float last_f;
float f;
float temp_rate;
float base_f;
/////////////////////////////////////////////////

//////////////////Timer Variables
const int onbutton = 9; //Symbolizes parent out of range of BLE
const int offbutton = 8; //Parent has returned and interacted with child
int second = 0;
int minute =0;
int base_min=0;
int iterated_base_min=0;
int onState = 0; //Variable for reading on button status
int offState = 0; //Variable for reading off button status
int timer_speed = 1000; //timer iterates 1/second
/////////////////////////////////////////////////

///////////////SMS Variables/functions
char replybuffer[255];
SoftwareSerial fonaSS = SoftwareSerial(FONA_TX, FONA_RX);
Adafruit_FONA fona = Adafruit_FONA(FONA_RST);
uint8_t readline(char *buff, uint8_t maxbuff, uint16_t timeout = 0);
/////////////////////////////////////////////////

void setup() {
  getReadyTempSens();
  getReadySMS();
  pinMode(onbutton, INPUT_PULLUP); // ONBUTTON is input with PULLUP = default is HIGH
  pinMode(offbutton, INPUT_PULLUP); //OFFBUTTON is input with PULLUP = default is HIGH

}

void loop() {
  onState = digitalRead(onbutton); //Reads status of on_button
  offState = digitalRead(offbutton); //Reads status of off_button
  int lastOnState;
  if(onState == LOW && offState == HIGH) { //If on_button is pressed...
    Serial.print("Timer was turned ON. \n");
        
    while (offState == HIGH){ //Parent still hasn't returned
      TemperatureSensor();
      timer();
      offState = digitalRead(offbutton); //Reads status of off_button
    }
  }
  
  if(offState == LOW && onState == HIGH) { //If off_button is pressed (Parent has returned)...
      Serial.print("Timer was turned OFF. \n");
      delay(timer_speed);
      second=0;
      minute=0;
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

void getReadyTempSens(){
  Serial.begin(115200);
  Serial.println("MCP9808 demo");
  if (!tempsensor.begin()) {
    Serial.println("Couldn't find MCP9808!");
    while (1);
  }
}  

void TemperatureSensor(){
  float f = tempsensor.readTempF();
  Serial.print("Temp: "); Serial.print(f); Serial.println("*F");

  if (last_f==0){ 
    last_f=f; //erase base value
    base_f=f; //set base_f at minute=0
  }  
  
  iterated_base_min=base_min+1;

  if (minute==iterated_base_min){
    base_min=base_min+1; //update base_min
    iterated_base_min+1; //update iterated_base_min
    base_f=last_f; //update base_f
  }
  
  rate(base_f,f);
  
  if (f>max) { //if ambient temp is too hot, send SMS
    HotCarSMS();
  }
  
  last_f=f; //update last_f before taking next temperature measurement
}

void rate(float base_f,float f) {
  temp_rate = f - base_f; //difference between current and base temperature
  
  if (temp_rate>danger){ //if temperature is rising dangerously fast send alert
    RateSMS();
  }
}

void RateSMS()
{
   char sendto[21]="8327978415";
   char message[141] = "Your child has been left in the car and the temperature is rising rapidly. Return to your car immediately.";

   flushSerial();

   if (!fona.sendSMS(sendto,message)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
}

void HotCarSMS(){
   char sendto[21]="8327978415";
   char message[141] = "Your child has been left in a hot car. Return to your car immediately.";
   
   flushSerial();
 
   if (!fona.sendSMS(sendto,message)) {
      Serial.println(F("Failed"));
   } 
   
   else {
      Serial.println(F("Sent!"));
   }
}

void WarningSMS() {
   char sendto[21]="8327978415";
   char message[141]="Your child is alone in a hot car. Please return to your car. EMS will be contacted in 60 seconds.";
   
   flushSerial();

   if (!fona.sendSMS(sendto, message)) {
      Serial.println(F("Failed"));
   } else {
      Serial.println(F("Sent!"));
   }
}

void AlertSMS() {
   char sendto[21]="8327978415";
   char message[141]="Your child has been alone in a hot car for an extended period of time. EMS has been contacted with your location.";
  
   flushSerial();

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

void timer() {
  delay(timer_speed); //wait for 1s
  second = second+1;
  
  if (second > 59) {
    minute=minute +1;
    second =0;
  }
   
   if (minute==3 && second==0){
      WarningSMS();
   }
   
   if (minute==4 && second==0){
      AlertSMS();
   }  
  print_time();
}

void print_time(){
  Serial.print("\n"); Serial.print(minute); Serial.print(":");   
  if (second<10){
    Serial.print("0");
  }
  Serial.print(second); Serial.print("\n");
}


