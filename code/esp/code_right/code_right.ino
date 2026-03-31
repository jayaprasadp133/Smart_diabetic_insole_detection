#include <WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// ---------------- WIFI ----------------
const char* ssid = "AirFiber-Rov1ne";
const char* password = "mahBeegahY9quo9O";

// Static IP configuration
IPAddress local_IP(192,168,31,201);
IPAddress gateway(192,168,31,1);
IPAddress subnet(255,255,255,0);
IPAddress primaryDNS(8,8,8,8);
IPAddress secondaryDNS(8,8,4,4);

WiFiServer server(80);

// ---------------- FSR PINS ----------------
int fsr1 = 35;   // Heel
int fsr2 = 33;   // Midfoot
int fsr3 = 34;   // Ball
int fsr4 = 32;   // Toe

// ---------------- TEMPERATURE SENSOR ----------------
#define ONE_WIRE_BUS 25
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

float skinTemp = 0;

void setup()
{
  Serial.begin(115200);
  delay(1000);

  Serial.println("RIGHT FOOT ESP32 STARTING...");

  pinMode(fsr1, INPUT);
  pinMode(fsr2, INPUT);
  pinMode(fsr3, INPUT);
  pinMode(fsr4, INPUT);

  sensors.begin();

  // Set ESP32 as WiFi station
  WiFi.mode(WIFI_STA);

  // Configure static IP
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS))
  {
    Serial.println("Static IP configuration FAILED");
  }

  // Connect to WiFi
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected!");

  Serial.print("RIGHT FOOT ESP32 IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop()
{
  // Read FSR sensors
  int p1 = analogRead(fsr1);
  int p2 = analogRead(fsr2);
  int p3 = analogRead(fsr3);
  int p4 = analogRead(fsr4);

  // Read temperature
  sensors.requestTemperatures();
  skinTemp = sensors.getTempCByIndex(0);

  // Serial debug
  Serial.print("Heel: "); Serial.print(p1);
  Serial.print(" Midfoot: "); Serial.print(p2);
  Serial.print(" Ball: "); Serial.print(p3);
  Serial.print(" Toe: "); Serial.print(p4);
  Serial.print(" SkinTemp: "); Serial.println(skinTemp);

  // Send data to Python
  WiFiClient client = server.available();

  if (client)
  {
    String data = String(p1) + "," +
                  String(p2) + "," +
                  String(p3) + "," +
                  String(p4) + "," +
                  String(skinTemp);

    client.println(data);
    client.stop();
  }

  delay(100);
}