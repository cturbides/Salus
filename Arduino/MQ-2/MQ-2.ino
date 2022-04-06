#define MQ2pin (0)

float sensorValue;  //variable to store sensor value

void setup()
{
  Serial.begin(9600); // sets the serial port to 9600
  Serial.println("Gas sensor warming up!");
  delay(20000); // allow the MQ-6 to warm up
}

void loop()
{
  sensorValue = analogRead(MQ2pin); // read analog input pin 0
  
  Serial.print("Sensor Value: ");
  Serial.print(sensorValue);
  
  if(sensorValue > 300)
  {
    Serial.print(" | Smoke detected!");
  }
  
  Serial.println("");
  delay(2000); // wait 2s for next reading
}


/*
 void setup() {
 Serial.begin(9600);
}
void loop() {
 float sensor_volt;
 float RS_gas; // Get value of RS in a GAS
 float ratio; // Get ratio RS_GAS/RS_air
 int sensorValue = analogRead(A0);
 sensor_volt=(float)sensorValue/1024*5.0;
 RS_gas = (5.0-sensor_volt)/sensor_volt; // omit *RL
 
 ratio = RS_gas/R0; // ratio = RS/R0
 Serial.print("sensor_volt = ");
 Serial.println(sensor_volt);
 Serial.print("RS_ratio = ");
 Serial.println(RS_gas);
 Serial.print("Rs/R0 = ");
 Serial.println(ratio);
 Serial.print("\n\n");
 delay(1000);
} 
*/
 
