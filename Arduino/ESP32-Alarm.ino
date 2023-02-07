#include <WiFi.h>
#include <HTTPClient.h>
#define CONNECTION_TIMEOUT 10
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701
#define PROXIMITY 10

const char* ssid = "**********";
const char* password = "********";
const char* host = "**.**.**.**"
const int port = 3000;  
const int trigPin = 5;
const int echoPin = 18;

long duration;
float distanceInch;


void setup() {
  Serial.begin(115200);
  Serial.println("-----  Start  -----");
  setupWiFi();
  setupGPIO();
  Serial.println();
}

/*
 * Setup and Connect to WiFi
 */
void setupWiFi() {
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.println("\nConnecting");

    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
}

/*
 * Setup GPIO for HC-SR04 Sensor
 */
void setupGPIO(){
   pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 
}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH); // Reads the echoPin, returns the sound wave travel time in microseconds
  distanceInch = (duration * SOUND_SPEED/2) * CM_TO_INCH; // Convert to inches

  if(distanceInch <= PROXIMITY && distanceInch > 0){
    HTTPClient http;

    http.begin("http://" + String(host) + ":" + String(port) + "/detect");
    http.addHeader("Content-Type", "application/json");
    http.POST("{\"distance\": " + String(distanceInch) + "}");

    int httpCode = http.GET();
    if (httpCode > 0) {
      String response = http.getString();
      Serial.println(response);
    } else 
      Serial.println("Error sending HTTP request: " + http.errorToString(httpCode));

    http.end();
    
    Serial.println("Proximity Breached");
    Serial.print("Distance (inch): ");
    Serial.println(distanceInch);
  }  
  delay(250);
}
