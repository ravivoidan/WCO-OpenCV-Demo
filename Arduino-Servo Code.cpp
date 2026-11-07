
#include <Servo.h>

Servo myservo;  // create Servo object to control a servo
// twelve Servo objects can be created on most boards

int pos = 90;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the Servo object

  myservo.write(pos);
  
  // Start serial communication with Python
  // The baud rate must match Python's baud rate
  Serial.begin(9600);

}

void loop() {
  if(Serial.available() > 0){
    // Read the number sent by Python
    // Python sends the number followed by a newline character
    pos = Serial.parseInt();

    // Make sure the servo position stays between 0 and 180 degrees
    pos = constrain(pos, 0, 180);

    // Move the servo to the received position
    myservo.write(pos);
    
    // Send the current servo position back to Python
    Serial.print("Servo position: ");
    Serial.println(pos);

  }
  

}
