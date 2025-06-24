#include <Servo.h>

Servo myServo;
const int ledPin = 8;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);            // Servo on pin 9
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);   // LED always ON for background noise
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    if (command == 'o') {
      // "Open" sound → move servo to 0°
      myServo.write(0);
    } else if (command == 'c') {
      // "Close" sound → move servo to 90°
      myServo.write(90);
    } else if (command == 'b') {
      // "Background noise" → no servo action (LED already ON)
      // Optional: return to neutral
      myServo.write(45); // or leave unchanged
    }
  }
}
