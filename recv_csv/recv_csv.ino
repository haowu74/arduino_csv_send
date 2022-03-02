String str;
String channel;
int comma;

int channel1 = 0;
int channel2 = 0;
int output1 = 0;
int output2 = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(output1,OUTPUT);
  pinMode(output2,OUTPUT);
}



void loop() {
  // put your main code here, to run repeatedly:
  str = Serial.readString();
  
  channel = str.substring(0, 8);

  if (channel == "Channel1")
  {
    comma = str.indexOf(',', 8);
    channel1 = str.substring(9, comma).toInt();
  }
  else
  {
    comma = str.indexOf(',', 8);
    channel2 = str.substring(9, comma).toInt();
  }

  analogWrite(output1,channel1);
  analogWrite(output2,channel2);
  delayMicroseconds(10);
}
