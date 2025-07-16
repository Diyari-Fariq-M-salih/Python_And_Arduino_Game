void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);  // Button
}

void loop() {
  int x = analogRead(A0);
  int y = analogRead(A1);
  int button = digitalRead(2);

  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.println(button);

  delay(100);  // Reduce if needed
}
