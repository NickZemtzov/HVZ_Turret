/* HVZ Integration
How this will work is the Arduino waits until the Odroid sends an 8 bit number.
That number is scanned to ensure it's the proper format - sometimes the numbers get a bit reversed or offset
That number will be one of six instructions:
1. Rotate horizontally: an identifier byte followed by a number representing how much to rotate
2. Rotate vertically: same format same idea but for the vertical servo
3. Rev the motor: just the identifier bit
4. Stop the motor: just the identifier bit
5. Fire: just the identifier bit, do the firing sequence
6. Reload: just the identifier bit, do the reloading sequence
*/

#include <Servo.h>

// SERVO CONTROLS
Servo HorizontalServo;  // Pin 9/yellow ring wire
Servo VerticalServo;  // Pin 3
int VerticalLower = 30;
int VerticalUpper = 85;
Servo FiringServo;  // Pin 11
int FiringLower = 50;
int FiringUpper = 160;
Servo ReloadingServo;  // Pin 10/black ring wire
// Continuous motion servos have 40 to 140 with 40 being max speed clockwise and 90 being no movement

// GPIO
const int flywheels = 2;

byte buf[1];

int pos = 0;

void FlywheelControl(bool state) {
  if (state) {
    digitalWrite(flywheels, HIGH);
  } else {
    digitalWrite(flywheels, LOW);
  }
}

void SpinUpFlywheels() {
  delay(1000);
  FlywheelControl(true);
  delay(1000);
  FlywheelControl(false);
  delay(1000);
}

void Fire() {
  for (pos = FiringLower; pos <= FiringUpper; pos += 1) {
    FiringServo.write(pos);
    delay(10);
  }
  for (pos = FiringUpper; pos >= FiringLower; pos -= 1) {
    FiringServo.write(pos);
    delay(10);
  }
}

void VerticalMovementRange() {
  for (pos = VerticalLower; pos <= VerticalUpper; pos += 1) {
    VerticalServo.write(pos);
    delay(30);
  }
  for (pos = VerticalUpper; pos >= VerticalLower; pos -= 1) {
    VerticalServo.write(pos);
    delay(30);
  }
}

void Reload() { // Needs some component fixes - change the rotator to just cover the hole and uncover to let balls through
  ReloadingServo.write(70);
  delay(1000);
  ReloadingServo.write(110);
  delay(1000);
  ReloadingServo.write(90);
}

void setup() {
  // Set up serial communication
  Serial.begin(115200);
  Serial.setTimeout(1);

  //Servo setup
  HorizontalServo.attach(10);
  VerticalServo.attach(3);
  VerticalServo.write(60);
  FiringServo.attach(11);
  ReloadingServo.attach(9);  

  // GPIO setup
  pinMode(flywheels, OUTPUT);
  digitalWrite(flywheels, LOW);

}

void loop() {
  // A character is sent over serial to the arduino and is stored in the byte buffer.
  // Then compare the byte to an int to decode it - e.g. ASCII 0 is 110000 so it equals 48 the integer
  // The input should be for example 0A to make the reloader write 65
  /* Table of encodings:
  0<anything> reload
  1<anything> rev flywheels
  2<anything> stop flywheels
  3<anything> fire
  4<byte> write the byte to the vertical servo
  5<byte> move the horizontal servo for byte amount of miliseconds
  */
  while (!Serial.available());
  int buflen = Serial.readBytes(buf, 1);
  if (buf[0] == 48) {                         //0X: Reload
    Reload();
    Serial.print(buf[0], DEC);
  } else if (buf[0] == 49) {                  //1X: Rev flywheels
    SpinUpFlywheels();
    Serial.print(buf[0], DEC);
  } else if (buf[0] == 50) {                  //2X: Stop flywheels
    digitalWrite(flywheels, LOW);
    Serial.print(buf[0], DEC);
  } else if (buf[0] == 51) {                  //3X: Fire
    Fire();
    Serial.print(buf[0], DEC);
  } else if (buf[0] == 52) {                  //4<byte>: Write the byte to the vertical servo
    while (!Serial.available());
    int buflen = Serial.readBytes(buf, 1);
    VerticalServo.write(buf[0]);
    Serial.print(buf[0], DEC);
  } else if (buf[0] == 53) {                  //5<byte>: Do stuff with the horizontal servo
    while (!Serial.available());
    int buflen = Serial.readBytes(buf, 1);
    HorizontalServo.write(buf[0]);
    Serial.print(buf[0], DEC);
    //TODO make this a function of time instead
  } else {
    Serial.print("R");
  }
}
