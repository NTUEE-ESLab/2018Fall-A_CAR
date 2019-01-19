#include <SoftwareSerial.h>

SoftwareSerial BTSerial(10, 11); // TXD,RXD of HC-05 bluetooth device
char input;
void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
}
void loop()
{
    // read state from the remote client and send controlling commands of local user
    if(Serial.available()>0){
      input = Serial.read();
      Serial.print(input);
      BTSerial.write(input);
      }
    delay(10);
}
