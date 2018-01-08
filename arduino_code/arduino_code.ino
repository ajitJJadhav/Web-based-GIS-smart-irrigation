#include <dht.h>
dht DHT;

#define DHT11_PIN 2
const int analogInPin = A4;
const int trigPin = 5;//9
const int echoPin = 6;//10
int sensor_pin = A0,sensor_pin2 = A1;
long duration;
int distance;

void setup(void) {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT);  // Sets the echoPin as an Input
  pinMode(7, OUTPUT);  //Motor 1
  pinMode(8, OUTPUT);  //motor 2
  Serial.begin(9600);
}

void ultrasonic() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  Serial.println((distance/30)*100);
}



void loop(void) {   
   int soil_moisture ,soil_moisture1;
   int sensorValue = 0;

  
   DHT.read11(DHT11_PIN);
   soil_moisture = analogRead(sensor_pin);       //soil moisture 1
   soil_moisture = map(soil_moisture,550,0,0,100);
   soil_moisture1= analogRead(sensor_pin2);      //soil moisture 2
   soil_moisture1= map(soil_moisture1,550,0,0,100);
   sensorValue  = analogRead(analogInPin);
   
   Serial.print(DHT.humidity);                //Humidity
   Serial.print(" ");
   Serial.print(DHT.temperature);            // temperat
   Serial.print(" "); 
   Serial.print(soil_moisture);
   Serial.print(" ");
   Serial.print(soil_moisture1);
   Serial.print(" ");
   if(sensorValue*100/1024 >= 0)             // rain gauge
      Serial.print(0);
   else
      Serial.print(1);
   Serial.print(" ");
                                                         // actuator trigering
   if(soil_moisture < -5 && sensorValue*100/1024 >= 0)
      digitalWrite(7,HIGH);
   else 
      digitalWrite(7,LOW);
    
   if(soil_moisture1 < -5 && sensorValue*100/1024 >= 0)
      digitalWrite(8,HIGH);
   else 
      digitalWrite(8,LOW);

   ultrasonic();                                     //ultrasonic for water level
   delay(6000);
}
