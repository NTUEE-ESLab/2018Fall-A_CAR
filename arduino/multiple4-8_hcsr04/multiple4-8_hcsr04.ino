#include <NewPing.h>

#define SONAR1 8
#define SONAR2 9
#define SONAR3 10
#define SONAR4 11
#define MAX_DISTANCE 300 // maximum distance for sensors
#define NUM_SONAR  4// number of sonar sensors 
 
NewPing sonar[NUM_SONAR] = { // array of sonar sensor objects
  NewPing(SONAR1, SONAR1, MAX_DISTANCE),
  NewPing(SONAR2, SONAR2, MAX_DISTANCE),
  NewPing(SONAR3, SONAR3, MAX_DISTANCE),
  NewPing(SONAR4, SONAR4, MAX_DISTANCE)};
int distance[NUM_SONAR]; // array stores distances for each
                         // sensor in cm
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  delay(1);
  updateSonar(); // update the distance array
  // print all distances
  Serial.print("S4: ");
  Serial.print(distance[0]);
  Serial.print("  S5: ");
  Serial.print(distance[1]);
  Serial.print("  S6: ");
  Serial.print(distance[2]);
  Serial.print("  S7: ");
  Serial.println(distance[3]);
  Serial.println();
}
 
// takes a new reading from each sensor and updates the
// distance array
void updateSonar() {
  for (int i = 0; i < NUM_SONAR; i++) {
    distance[i] = sonar[i].ping_cm(); // update distance
    // sonar sensors return 0 if no obstacle is detected
    // change distance to max value if no obstacle is detected
    if (distance[i] == 0 || distance[i] > MAX_DISTANCE)
      distance[i] = MAX_DISTANCE;
  }
}
