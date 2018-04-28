const int onbutton = 9; //Symbolizes parent out of range of BLE
const int offbutton = 8; //Parent has returned and interacted with child
int second = 0;
int minute =0;
int onState = 0; //Variable for reading on button status
int offState = 0; //Variable for reading off button status

void setup() {
  Serial.begin(115200);
  pinMode(onbutton, INPUT_PULLUP); // ONBUTTON is input with PULLUP = default is HIGH
  pinMode(offbutton, INPUT_PULLUP); //OFFBUTTON is input with PULLUP = default is HIGH

}

void loop() {
  onState = digitalRead(onbutton); //Reads status of on_button
  offState = digitalRead(offbutton); //Reads status of off_button
  if(onState == LOW && offState == HIGH) { //If on_button is pressed...
    Serial.print("Timer was turned ON. \n");
    while (offState == HIGH){
      timer();
      offState = digitalRead(offbutton); //Reads status of off_button
    }
  }
  
  if(offState == LOW && onState == HIGH) { //If off_button is pressed...
      Serial.print("Timer was turned OFF. \n");
      delay(1000);
      second=0;
      minute=0;
  }
}  
void timer() {
  delay(1000); //wait for 1s
  second = second+1;
  
  if (second > 59) {
    minute=minute +1;
    second =0;
  }
  
  print_time();
}

void print_time(){
  Serial.print(minute); Serial.print(":");   
  if (second<10){
    Serial.print("0");
  }
  Serial.print(second); Serial.print("\n");
}


