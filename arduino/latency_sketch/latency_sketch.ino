#include <Arduino.h>

// Pin assignments:
const int pressPin = 2;         // Manual press sensor (wired so that contact pulls the pin LOW)
const int sensorPin = A0;       // Light sensor input (phototransistor voltage divider)
const int sensorThreshold = 5; // Adjust this threshold based on your calibration

// Define a simple state machine:
enum State {
  WAIT_FOR_PRESS,
  WAIT_FOR_SENSOR,
  WAIT_FOR_RELEASE
};

State currentState = WAIT_FOR_PRESS;
unsigned long startTime = 0;

void setup() {
  Serial.begin(115200);
  pinMode(pressPin, INPUT_PULLUP);  // Use internal pull-up
}

void loop() {
  if (currentState == WAIT_FOR_PRESS) {
    if (digitalRead(pressPin) == LOW) {
      // Record start time as soon as a press is detected
      startTime = micros();
      currentState = WAIT_FOR_SENSOR;
      // Serial.println("KEY PRESSED");
    }
  }
  else if (currentState == WAIT_FOR_SENSOR) {
    // Poll the sensor until the reading exceeds the threshold.
    int sensorMeasure = analogRead(sensorPin);
    if (sensorMeasure >= sensorThreshold) {
      unsigned long endTime = micros();
      unsigned long latency = endTime - startTime;
      // Send the raw latency (in microseconds) over Serial.
      // Serial.println("SENSOR");
      // Serial.println(sensorMeasure);
      // Serial.println("LATENCY");
      Serial.println(latency);
      currentState = WAIT_FOR_RELEASE;
    }
  }
  else if (currentState == WAIT_FOR_RELEASE) {
    // Wait until the press is released before starting a new measurement.
    if (digitalRead(pressPin) == HIGH) {
      currentState = WAIT_FOR_PRESS;
    }
  }
}

