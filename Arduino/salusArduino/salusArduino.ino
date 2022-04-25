//Imports & libraries needed!
#include <DHT_U.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <MQUnifiedsensor.h>
#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
#include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library.   

//Define block
#define DHTPIN 2                       // Digital Pin -> 2
#define DHTTYPE  DHT11                 // Sensor Type
#define placa "Arduino MEGA"
#define Voltage_Resolution 5
#define pin A0                         // A0
#define type "MQ-135"                  // MQ135
#define ADC_Bit_Resolution 10
#define RatioMQ135CleanAir 3.6
#define electromiography A1            // A1

//Constants
const int PulseWire = 5;               // PulseSensor PURPLE WIRE connected to ANALOG PIN 5
const int Paciente_temperatura = 36;   // Fixed Value
const int roomDust = 60;               // Fixed Value
const int LED13 = 13;                  // On-board Arduino LED

//Variables
int pulso; 
int Threshold = 550;                   //PulseSensor
float calcR0 = 192.08;                 // MQ-135 R0 value
float oldValue_airQuality;             // First airQuality value saved
float newValue_airQuality;    
bool flag = false;                     // Flag used to determine if oldValue_airQuality was saved
int count = 0;
uint32_t delayMs = 500;                // Delay in microseconds

//Instances block
DHT_Unified dht(DHTPIN, DHTTYPE);
MQUnifiedsensor MQ135(placa, Voltage_Resolution, ADC_Bit_Resolution, pin, type);
PulseSensorPlayground pulseSensor; 

void setup() {
  Serial.begin(9600);
  
  //Initializing all sensor variables
  dht.begin();                         // DHT-11 Initialization
  MQ135.setRegressionMethod(1);
  MQ135.init();                        // MQ-135 Initialization
  MQ135.setR0(calcR0/10);
   
  pulseSensor.analogInput(PulseWire);  // Making On-board Arduino LED part of PulseSensor instance
  pulseSensor.blinkOnPulse(LED13);     //auto-magically blink Arduino's LED with heartbeat.
  pulseSensor.setThreshold(Threshold); // Setting Threshold value equal to our threshold variable
  pulseSensor.begin();                 // PulseSensor Initialization
}

void loop() {
  count++;                             // Add 1 every cycle
  MQ135.update();                      // Update MQ-135 values
  delay(delayMs);                      // Some delay between cycles

  // MQ-135 block
  MQ135.setA(605.18); MQ135.setB(-3.937); // Configurate the ecuation values to get CO concentration
  float CO = MQ135.readSensor();          // Sensor will read PPM concentration using the model and a and b values setted before or in the setup

  MQ135.setA(77.255); MQ135.setB(-3.18);  // Configurate the ecuation values to get Alcohol concentration
  float Alcohol = MQ135.readSensor();

  MQ135.setA(110.47); MQ135.setB(-2.862); // Configurate the ecuation values to get CO2 concentration
  float CO2 = MQ135.readSensor(); 

  MQ135.setA(44.947); MQ135.setB(-3.445); // Configurate the ecuation values to get Tolueno concentration
  float Tolueno = MQ135.readSensor();

  MQ135.setA(102.2 ); MQ135.setB(-2.473); // Configurate the ecuation values to get NH4 concentration
  float NH4 = MQ135.readSensor(); 

  MQ135.setA(34.668); MQ135.setB(-3.369); // Configurate the ecuation values to get Acetona concentration
  float Acetona = MQ135.readSensor(); 

  // Is the first program cycle?
  if (!flag){
    oldValue_airQuality = Acetona + NH4 + Tolueno + CO2 + Alcohol + CO; //  Save the first value sensed
    flag = true;
  }
  //  -> If not the first time
  else {
    sensors_event_t event;               // Event Pointer for DHT-11 values
    dht.temperature().getEvent(&event);  // Getting the temperature event throwed value
    Serial.print(event.temperature);     // Printing Temperature
    Serial.print(" ");
    Serial.print(Paciente_temperatura);  // Fixed value          
    Serial.print(" ");
    dht.humidity().getEvent(&event);     // Getting the humidity event throwed value
    Serial.print(event.relative_humidity);
    Serial.print(" ");
    Serial.print(roomDust);              // Fixed value 
    Serial.print(" ");
    newValue_airQuality = Acetona + NH4 + Tolueno + CO2 + Alcohol + CO;
    newValue_airQuality = (newValue_airQuality/oldValue_airQuality)*100; //Air quality
    Serial.print(newValue_airQuality);   // Printing Air Quality value
    Serial.print(" ");
    int myBPM = pulseSensor.getBeatsPerMinute(); 
    Serial.print(myBPM);                 // Printing Beats per minute
    Serial.print(" ");
    Serial.println(analogRead(electromiography));
    }
}
