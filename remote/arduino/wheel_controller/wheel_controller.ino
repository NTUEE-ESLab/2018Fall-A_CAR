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
int PWM_in = 3;
int PWM_freq = 50;
int PWM_value = 0;

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
  pinMode(PWM_in, INPUT);
  
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

  if (left == right){
    if (front > 0){
      left_speed += 150;
      right_speed += 150;
    }
    if (back > 0){
      left_speed -= 100;
      right_speed -= 100;
    }
  }
  else if (left > 0){
    if (back > 0 && front == 0){
      left_speed = -40;
      right_speed = -250;
    }
    else if (front == 0 && back == 0){
      left_speed = -180;
      right_speed = 180;
    }
    else{
      left_speed = 40;
      right_speed = 250;
    }
  }
  else if (right > 0){
    if (back > 0 && front == 0){
      left_speed = -230;
      right_speed = -40;
    }
    else if (front == 0 && back == 0){
      left_speed = 180;
      right_speed = -180;
    }
    else{
      left_speed = 230;
      right_speed = 40;
    }
  }
  
  if (front > 0 && back > 0 && left > 0 && right > 0){
    left_speed = 255;
    right_speed = 255;
  }

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
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    analogWrite(enB, right_speed);
  }
  else if (right_speed < 0){
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    analogWrite(enB, -right_speed);
  }
  else{ 
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
    analogWrite(enB, right_speed);
  }

  delay(20);
}

void loop()
{
  float sum = 0;
  
  // the commands from the local end are encoded to PWM signals
  // averaging across the values received to get higher accuracy
  for(int i = 0; i < 5; i++){
    sum += pulseIn(PWM_in, HIGH);
  }
  float mean = sum / 5;
  
  PWM_value = int(round(mean / 1000000 * PWM_freq * 18 - 2.5));
  PWM_value = max(PWM_value, 0);
  PWM_value = min(PWM_value, 15);
  
  // transmit the signal to the motors
  demoOne(PWM_value);
  Serial.println(PWM_value);
  delay(20);
}
