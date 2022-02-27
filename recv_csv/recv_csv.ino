String str;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(96000);
  Serial.println("Hello world!");
}



void loop() {
  // put your main code here, to run repeatedly:
  str = Serial.readString();
  Serial.println(str);
  delay(1);
}
