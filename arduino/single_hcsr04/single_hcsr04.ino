#include <NewPing.h>
 
#define TRIGGER_PIN 2
#define ECHO_PIN 2
#define MAX_DISTANCE 400 // max distance the sensor will return
 
NewPing sonar(11, 11, MAX_DISTANCE); // declare a NewPing object
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  delay(1);
  int uS = sonar.ping(); 
  Serial.print("Ping: ");
  Serial.print(uS / US_ROUNDTRIP_CM); // convert ping time to distance in cm
  Serial.println("cm");
}
