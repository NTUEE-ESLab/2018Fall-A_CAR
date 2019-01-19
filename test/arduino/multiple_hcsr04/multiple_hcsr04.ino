#include <NewPing.h>

#define SONAR1 7
#define SONAR2 6
#define SONAR3 5
#define SONAR4 4
#define MAX_DISTANCE 400 // maximum distance for sensors
#define NUM_SONAR  4// number of sonar sensors 
 
NewPing sonar[NUM_SONAR] = { // array of sonar sensor objects
  NewPing(SONAR1, SONAR1, MAX_DISTANCE),
  NewPing(SONAR2, SONAR2, MAX_DISTANCE),
  NewPing(SONAR3, SONAR3, MAX_DISTANCE),
  NewPing(SONAR4, SONAR4, MAX_DISTANCE)};
  //NewPing(SONAR5, SONAR5, MAX_DISTANCE),
  //NewPing(SONAR6, SONAR6, MAX_DISTANCE),
  //NewPing(SONAR1, SONAR8, MAX_DISTANCE),
  //NewPing(SONAR1, SONAR9, MAX_DISTANCE)
//};
 
int distance[NUM_SONAR]; // array stores distances for each
                         // sensor in cm
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  delay(1000);
  updateSonar(); // update the distance array
  // print all distances
  Serial.print("S0: ");
  Serial.print(distance[0]);
  Serial.print("  S1: ");
  Serial.print(distance[1]);
  Serial.print("  S2: ");
  Serial.print(distance[2]);
  Serial.print("  S3: ");
  Serial.println(distance[3]);
  //Serial.print("  S6: ");
  //Serial.print(distance[4]);
  //Serial.print("  S7: ");
  //Serial.println(distance[5]);
  //Serial.print("  S8: ");
  //Serial.print(distance[6]);
  //Serial.print("  S9: ");
  //Serial.print(distance[7]);
  //Serial.println();
  //for(int i=0;i<8;i++){
    //if(distance[i] != MAX_DISTANCE){
      //Serial.print("1  ");
      //}
    //else{
      //Serial.print("0  ");
      //}
    //}
  //Serial.println();
  Serial.println();
}
 
// takes a new reading from each sensor and updates the
// distance array
void updateSonar() {
  for (int i = 0; i < NUM_SONAR; i++) {
    distance[i] = sonar[i].ping_cm(); // update distance
    // sonar sensors return 0 if no obstacle is detected
    // change distance to max value if no obstacle is detected
    if (distance[i] == 0)
      distance[i] = MAX_DISTANCE;
  }
}
