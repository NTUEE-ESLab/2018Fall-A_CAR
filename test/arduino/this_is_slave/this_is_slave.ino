#include <Wire.h>
#include <SoftwareSerial.h>
SoftwareSerial BTSerial(12, 13); // HC-05的TXD,RXD腳位
char a;
int enA = 10;
int in1 = 9;
int in2 = 8;
// motor two
int enB = 5;
int in3 = 7;
int in4 = 6;
void setup()
{
  Serial.begin(9600);
  BTSerial.begin(9600);
    // set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}
void demoOne(char a)
{
  // this function will run the motors in both directions at a fixed speed
  // turn on motor A
  if(a == 'W'){
    //set A
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enA, 100);
    //set B
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    analogWrite(enB, 100);
  }
  else if(a == 'S'){
    //set A
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enA, 100);
    //set B
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    analogWrite(enB, 100);
    }
  else if(a == 'D'){
    //set A
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enA, 200);
    //set B
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    analogWrite(enB, 50);
    }
  else if(a == 'A'){
    //set A
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enA, 40);
    //set B
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    analogWrite(enB, 225);
    }
  else{
    //set A
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  // set speed to 200 out of possible range 0~255
    analogWrite(enA, 0);
    //setB
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
  // set speed to 200 out of possible range 0~255
    analogWrite(enB, 0);
    }
  // turn on motor B
  //digitalWrite(in3, HIGH);
  //digitalWrite(in4, LOW);
  // set speed to 200 out of possible range 0~255
  //analogWrite(enB, 200);
  delay(50);
  // now change motor directions
  /*
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);  
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH); 
  delay(2000);
  // now turn off motors
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);*/
}
void loop()
{
  // 檢查是否有資料傳來
  while (BTSerial.available()) {
    delay(10);  //稍候一下，讓資料都到
    a = BTSerial.read();
    //BTSerial.write(a);
    Serial.print(a);
    demoOne(a);
  }
}
