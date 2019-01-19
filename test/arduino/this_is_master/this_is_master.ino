#include <SoftwareSerial.h>
SoftwareSerial BTSerial(10, 11); // HC-05的TXD,RXD腳位
char input;
void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
  
  //稍等一秒後再送資料給遠方
  //BTSerial.write(1);
}
void loop()
{
    if(Serial.available()>0){
      input = Serial.read();
      Serial.print(input);
      BTSerial.write(input);
      }
    delay(10);
  /*while (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    BTSerial.write(incomingByte);
  }
  delay(1000);*/
}
