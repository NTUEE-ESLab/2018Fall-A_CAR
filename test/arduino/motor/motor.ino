#include <Wire.h>
#include <SoftwareSerial.h>

int value;
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
    // set all the motor control pins to outputs
  pinMode(enA, OUTPUT); // left
  pinMode(enB, OUTPUT); // right
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}
void demoOne(int value)
{
  // this function will run the motors in both directions
  
  // bool value of the keys pressed
  int front = value % 2;
  int back = (value % 4 > 1);
  int left = (value % 8 > 3);
  int right = (value % 16 > 7);
  
  int left_speed = 0; // of range 0~255
  int right_speed = 0;
  
  if (front > 0){
    left_speed += 150;
    right_speed += 150;
  }
  else if (back > 0){
    left_speed -= 80;
    right_speed -= 80;
  }
  else if (left > 0){
    left_speed -= 50;
    right_speed += 50;
  }
  else if (right > 0){
    left_speed += 50;
    right_speed -= 50;
  }
  if (front > 0 && back > 0 && left > 0 && right > 0){
    left_speed = 225;
    right_speed = 225;
  }
  Serial.print(value);
  Serial.print(left_speed);
  Serial.print(right_speed);
  Serial.print('\n');
  
  if (left_speed > 0){
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enA, left_speed);
  }
  else if (left_speed < 0){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enA, -left_speed);
  }
  else{ 
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    analogWrite(enA, left_speed);
  }
  
  if (right_speed > 0){
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enB, right_speed);
  }
  else if (left_speed < 0){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enB, -right_speed);
  }
  else{ 
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    analogWrite(enB, right_speed);
  }
  
  delay(50);
}

void loop()
{
  if(Serial.available()){
    // up, down, left and right commands are encoded as a character from 'A' to 'P' on the local end
    value = (Serial.read() - 'A');  // conveting the value of chars to integers  
    demoOne(value);
  }
  delay(10);
}
