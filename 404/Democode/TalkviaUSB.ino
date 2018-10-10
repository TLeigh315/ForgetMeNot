const int ledPin1 = 13;
const int ledPin2 = 9;
const int ledPin3 =8;

void setup() 
{
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  Serial.begin(9600); //determines data transfer rate. MUST be the same as baud rate in Rpi
}

void loop() 
{
 if(Serial.available())
 { //check if data is coming in from Rpi
    light((Serial.read()-'0')); //function we use to pass on Serial.read() data
 }
 delay(500); //give it time to read data
}

void light(int n)
{
  switch(n)
  {
    case 1:
    digitalWrite(ledPin1, HIGH);
    Serial.write("Green light on\n");
    delay(1000);
    digitalWrite(ledPin1,LOW);
    delay(1000);
    break;
    
    case 2:
    digitalWrite(ledPin2, HIGH);
    Serial.write("Yellow light on\n");
    delay(1000);
    digitalWrite(ledPin2,LOW);
    delay(1000);
    break;
    
    case 3:
    digitalWrite(ledPin3, HIGH);
    Serial.write("Red light on\n");
    delay(1000);
    digitalWrite(ledPin3,LOW);
    delay(1000);
    break;
  }
}

void flushSerial() {
    while (Serial.available()) 
    Serial.read();
}
