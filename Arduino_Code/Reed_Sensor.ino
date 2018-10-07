const int reed = 2;  //Pin Reed
const int pinLed    = 7;  //Pin LED
int switchState = 0;
void setup()
{
  Serial.begin(115200);
  pinMode(pinLed, OUTPUT); //LED is OUTPUT
  pinMode(reed, INPUT); //Reed Sensor is INPUT
}
void loop()
{
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
  }
  delay(1000);
}
