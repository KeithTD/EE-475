void setup() {
  // put your setup code here, to run once:
  Serial.begin (115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.write("a");
  char entry;
  if (Serial.available()) {
    entry = Serial.read();
    Serial.print(entry);
  }
  delay(1000);
}
