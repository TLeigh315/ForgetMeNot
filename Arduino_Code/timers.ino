int ledpin = 13;
int second = 0;
int minute =0;
void setup() {
  Serial.begin(115200);
  pinMode(ledpin, INPUT);
}

void loop() {
  
  digitalWrite(ledpin, HIGH);
  delay(1000); //wait for 1s
  second = second+1;
  timer();

  Serial.print(minute); Serial.print(":");   
  if (second<10){
    Serial.print("0");
  }
  
  Serial.print(second); Serial.print("\n");
  /*digitalWrite(ledpin, LOW);
  delay(1000); //wait for 1s
  second = second+1;
  timer();*/
}

void timer() {
  if (second > 59) {
    minute=minute +1;
    second =0;
  }
}

