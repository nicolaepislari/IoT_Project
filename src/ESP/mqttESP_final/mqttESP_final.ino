/*
   Remote Button Press

   This app is using ESP8266 NodeMCU to control a servo which performs an action to press a button.

   Hardware Requirement:
   - ESP8266 NodeMCU
   - 90g servo & connecting wires
   - power supply
   - materials help to fix the servo next to the button

   Software coding is divided into the following parts:
   - wifi setup
   - connection to MQTT server and subscribe to a topic
   - parse incoming message from the MQTT server
   - activate the servo to perform a press action
   - feedback to MQTT server when done
   - Can use <a href="https://eclipse.org/paho/clients/js/utility/" rel="nofollow">https://eclipse.org/paho/clients/js/utility/</a> for testing

*/

#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>
#include <PubSubClient.h>  // for MQTT connection
#include <ArduinoJson.h>   // to parse and encode JSON
#include <String.h>
#include <cstring>

const char* broker_host = "iot.eclipse.org";
const int broker_port = 1883;

// topics to subscribe
const char* pumpTopic = "/zone1/pump";
const char* fanTopic = "/zone1/fan";
const char* heaterTopic = "/zone1/heater";
const char* coolerTopic = "/zone1/cooler";

const char* outTopic = "greenhouse/status";


char msg[75];
long lastMsg = 0;
int value = 0;

int pumpPin = D0;
int fanPin  = D1;
int heaterPin = D2;
int coolerPin = D3;


WiFiClient espClient;
PubSubClient client(espClient);

WiFiManager wifiManager;

/*
   control the servo to mimic a button press action
   duration in seconds, posStart & posEnd in degrees
*/
void buttonPress() {
}

/*
   handle message arrived from MQTT and do the real actions depending on the command
   payload format: start with a single character
   P: button press, optionally follows by (in any order)
      Dxxx: for xxx seconds duration,
      Exxx: ending at xxx angle
   R: reset wifi settings
*/
void mqttCallback(char* topic, byte* payload, unsigned int length) {

  String recv_payload = "";  //variable to store the payload as String
  //  String my_msg = "";
  char my_msg[100];

  // debugging message at serial monitor
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    recv_payload  += (char)payload[i];  // create the string with the payload
  }
  //  Serial.println(recv_payload);

  // parse the payload message
  Serial.println();

  // Allocate JsonBuffer
  // Use arduinojson.org/assistant to compute the capacity.
  const size_t bufferSize = JSON_OBJECT_SIZE(4) + 100;
  DynamicJsonBuffer jsonBuffer(bufferSize);

  // Parse JSON object
  JsonObject& root = jsonBuffer.parseObject(recv_payload);

  if (strcmp(topic, pumpTopic) == 0) {
    String cmd = root["pump"];
    if (cmd == "1") {               // start the pump
      digitalWrite(pumpPin, HIGH);
      // digital write high
      Serial.println("Pump is on");
    }
    else if (cmd == "0") {          // stop the pump
      digitalWrite(pumpPin, LOW);
      // command for stop the pump
      Serial.println("Pump is off");
    }else {Serial.println("Invalid comand"); }
  }
  else if (strcmp(topic, fanTopic) == 0) {
    String cmd = root["fan"];
    if (cmd == "1") {               // start the fan
       digitalWrite(fanPin, HIGH);
      // digital write high
      Serial.println("Fan is on");
    }
    else if (cmd == "0") {         // stop the fan
      digitalWrite(fanPin, LOW);
      // command for stop the fan
      Serial.println("Fan  is off");
    }
  }
  else if (strcmp(topic, heaterTopic) == 0) {
    String cmd = root["heater"];
    if (cmd == "1") {                 // start the heater
      digitalWrite(heaterPin, HIGH);
      // digital write high
      Serial.println("heater is on");
    }
    else if (cmd == "0") {           // stop the heater
      digitalWrite(fanPin, LOW);
      // command for stop the heater
      Serial.println("heater  is off");
    }else {Serial.println("Invalid comand"); }
  }
  else if (strcmp(topic, coolerTopic) == 0) {
    String cmd = root["cooler"];
    if (cmd == "1") {               // start the cooler
      digitalWrite(coolerPin, HIGH);
      // digital write high
      Serial.println("cooler is on");
    }
    else if (cmd == "0") {          // stop the cooler
      digitalWrite(fanPin, LOW);
      // command for stop the cooler
      Serial.println("cooler  is off");
    }
    else {Serial.println("Invalid comand"); }
  } else {
    Serial.println("Invalid comand"); 
  }
}



/*
   connect to MQTT with a client ID, subscribe & publish to corresponding topics
   if failed, reconnect in 5 seconds
*/
void reconnect() {
  // loop until reconnected
  while (!client.connected()) {
    Serial.print("Attempting to make MQTT connection...");
    if (client.connect("ESP8266Client1")) {  // ESP8266CLient1 is a client ID of this ESP8266 for MQTT
      Serial.println("connected");
      client.publish(outTopic, "Hello world, I'm ESP8266Client1");
      client.subscribe(pumpTopic);
      Serial.print("Subscribed to: ");
      Serial.println(pumpTopic);

      client.subscribe(fanTopic);
      Serial.print("Subscribed to: ");
      Serial.println(fanTopic);

      client.subscribe(coolerTopic);
      Serial.print("Subscribed to: ");
      Serial.println(coolerTopic);

      client.subscribe(heaterTopic);
      Serial.print("Subscribed to: ");
      Serial.println(heaterTopic);




    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);  // just for LED output
  Serial.begin(115200);  // connect to serial mainly for debugging
  
  pinMode(pumpPin,OUTPUT);
  pinMode(fanPin,OUTPUT);
  pinMode(heaterPin,OUTPUT);
  pinMode(coolerPin,OUTPUT);

  digitalWrite(pumpPin,LOW);
  digitalWrite(fanPin,LOW);
  digitalWrite(heaterPin,LOW);
  digitalWrite(coolerPin,LOW);

  // use WiFiManger to manage wifi setup
  // if not auto connect, connect to 'myAP' wifi network, access 192.168.4.1 to do a local wifi setup
  wifiManager.autoConnect("myAP");
  Serial.println("wifi connected!");

  // prepare for MQTT connection
  client.setServer(broker_host, broker_port);
  client.setCallback(mqttCallback); // attach callback
}

void loop() {
  // if not connected to mqtt server, keep trying to reconnect
  if (!client.connected()) {
    reconnect();
  }
  client.loop();  // wait for message packet to come & periodically ping the server
  // to show that ESP8266 is alive, publish a message every 2 seconds to the MQTT broker
  
//  long now = millis();
//  if (now - lastMsg > 2000) {
//    lastMsg = now;
//    ++value;
//    snprintf(msg, 75, "Hello world #%ld", value);
//    Serial.print("Publish message: ");
//    Serial.println(msg);
//    client.publish(outTopic, msg);
//  }
}
