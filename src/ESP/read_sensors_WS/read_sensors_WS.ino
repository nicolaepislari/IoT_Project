

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WiFiMulti.h> 
#include <ESP8266mDNS.h>
#include <ESP8266WebServer.h>   // Include the WebServer library
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>


#include <OneWire.h>
//#include <DallasTemperature.h>
//#define ONE_WIRE_BUS 13 // D7 on board

 // Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
//OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
//DallasTemperature sensors(&oneWire);


ESP8266WiFiMulti wifiMulti;     // Create an instance of the ESP8266WiFiMulti class, called 'wifiMulti'

ESP8266WebServer server(80);    // Create a webserver object that listens for HTTP request on port 80

void handleRoot();              // function prototypes for HTTP handlers
void handleNotFound();
void handleStatus();
void handleCmd();




String payload = "";

// Auxiliar variables to store the current output state
  String output0State = "off";
  String output1State = "off";
  String output2State = "off";
  
// Assign output variables to GPIO pins
  const int output0 = 0;
  const int output1 = 1;
  const int output2 = 2;

  unsigned long previousMillis = 0;        // will store last time info was updated
  unsigned long previousMillis_sensors = 0;        // will store last time data was sent on MQTT
  // constants won't change :
  const long interval = 5000;           // interval to update info in catalog (milliseconds)
  const long interval_sensors = 30000;

void setup(void){
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');
  
  // Initialize the output variables as outputs
    pinMode(output0, OUTPUT);
    pinMode(output1, OUTPUT);
    pinMode(output2, OUTPUT);

  // Set outputs to LOW
    digitalWrite(output0, LOW);
    digitalWrite(output1, HIGH);   // inverted logic
    digitalWrite(output2, LOW);
    

  wifiMulti.addAP("InfostradaWiFi-f330b2", "8b84bf2c3abb4");   // add Wi-Fi networks you want to connect to
  wifiMulti.addAP("Redmi", "12345678");
//  wifiMulti.addAP("ssid_from_AP_3", "your_password_for_AP_3");

  Serial.println("Connecting ...");
  int i = 0;
  while (wifiMulti.run() != WL_CONNECTED) { // Wait for the Wi-Fi to connect: scan for Wi-Fi networks, and connect to the strongest of the networks above
    delay(250);
    Serial.print('.');
  }
  Serial.println('\n');
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());              // Tell us what network we're connected to
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());           // Send the IP address of the ESP8266 to the computer

  if (MDNS.begin("esp8266")) {              // Start the mDNS responder for esp8266.local
    Serial.println("mDNS responder started");
  } else {
    Serial.println("Error setting up MDNS responder!");
  }

  server.on("/", handleRoot);               // Call the 'handleRoot' function when a client requests URI "/"
  server.onNotFound(handleNotFound);        // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"
  server.on("/status", handleStatus);  
  server.on("/cmd", handleCmd);      
  server.on("/read",handleRead);



  server.begin();                           // Actually start the server
  Serial.println("HTTP server started");

  
  register_catalog();


}  // void setup end

void loop(void){
  server.handleClient();                    // Listen for HTTP requests from clients

  // repeat every 5 seconds
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;
    register_catalog(); 
  }
  ///////////////////////////////////////////////////////////////////////

  // repeat every 30 seconds   //////////////////////////////////////////
  currentMillis = millis();
  if (currentMillis - previousMillis_sensors >= interval_sensors) {
    // save the last time you blinked the LED
    previousMillis_sensors = currentMillis;
    
   /// readSensors 
  }
  //////////////////////////////////////////////////////////////////////
}

void handleRoot() {
  server.send(200, "text/plain", "Hello world!");   // Send HTTP status 200 (Ok) and send some text to the browser/client
}

void handleStatus() {
      String message = payload;
             message += "\n";
 
      server.send(200, "application/json", message);
}

void handleCmd(){

    const char* msg = "{\"status\":\"error\",\"message\":\"Invalid command: The request has empty body\"}";
    if (server.hasArg("plain")== false){ //Check if body received
        server.send(200, "application/json", msg);
        return;
      }

      String recv_payload = server.arg("plain");

      // Allocate JsonBuffer
      // Use arduinojson.org/assistant to compute the capacity.
      const size_t bufferSize = JSON_OBJECT_SIZE(4) + 100;
      DynamicJsonBuffer jsonBuffer(bufferSize);

      // Parse JSON object
      JsonObject& root = jsonBuffer.parseObject(recv_payload);

      String led_0 = root["led_0"]; // "on/off"
      if (led_0 == "on"){
        output0State = "on";
        digitalWrite(output0, HIGH); 
        msg = "{\"status\":\"success\",\"message\":\"led_0 is now ON\"}";
      } 
      else if (led_0 == "off"){
        output1State = "off";
        digitalWrite(output0, LOW); 
        msg = "{\"status\":\"success\",\"message\":\"led_0 is now OFF\"}";
      } 
      else {
        msg = "{\"status\":\"error\",\"message\":\"Invalid Command\"}";
      }



      
      server.send(200, "application/json", msg);
  }



void handleRead(){

    String msg; 
    const char* my_msg = "{\"status\":\"error\",\"message\":\"Invalid command: The request has empty body\"}";
    if (server.hasArg("plain")== false){ //Check if body received
        server.send(200, "application/json", my_msg);
        return;
      }

      String recv_payload = server.arg("plain");

      // Allocate JsonBuffer
      // Use arduinojson.org/assistant to compute the capacity.
      const size_t bufferSize = JSON_OBJECT_SIZE(4) + 100;
      DynamicJsonBuffer jsonBuffer(bufferSize);

      // Parse JSON object
      JsonObject& root = jsonBuffer.parseObject(recv_payload);

      String cmd = root["read"]; 
      if (cmd == "temp"){
        //msg temp
        float temp = readTemp();
        String temp_string = String(temp);
//        msg = "{\"status\":\"success\",\"message\":\"" + temp_string + "\"}";
        msg = "{\"status\":\"success\",\"temperature\":{\"value\":" +temp_string+ ",\"unit\":\"C\"}}";
      } 
      else if (cmd == "humi"){
        // msg = humi
        float humi = readHumi();
        String humi_string = String(humi);
        msg = "{\"status\":\"success\",\"humidity\":{\"value\":" +humi_string+ ",\"unit\":\"%\"}}";
      } 
      else if (cmd == "all"){

        msg = readAll();
        
      }
      else{
          msg = "{\"status\":\"error\",\"message\":\"Invalid Command\"}";
        }

      
      server.send(200, "application/json", msg);
  }


void handleNotFound(){
  const char* err_msg = "{\"status\":\"error\",\"message\":\"404: Not found\"}";
  server.send(404, "application/json", err_msg); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}




void register_catalog(){

  // send to catalog
  //{
  //  "type": "device",
  //  "deviceID": "ESP-01"
  //}
  
    String catalog_url = "http://192.168.1.18:8080/iamalive";  
    String ip = WiFi.localIP().toString();
      
    String reg_msg = "{\"type\":\"device\",\"deviceID\":\"ESP-01\",\"ip\":\""  + ip + "\"}";
  
    HTTPClient http;

    http.begin(catalog_url);      //Specify request destination
    http.addHeader("Content-Type", "text/plain");  //Specify content-type header
 
    int httpCode = http.POST(reg_msg);   //Send the request
    payload = http.getString();   //Get the response payload
    http.end();  //Close connection

// response from catalog 
  //  {
  //    "status": "registered",
  //    "data": {
  //        "last_update": "2018-09-11 11:50:49",
  //        "deviceID": "ESP-01",
  //        "type": "device"
  //    }
//  }
  
  }


float readTemp() {
  float tmp = 36.6;
  return tmp;
}

float readHumi() {
  float humi  = 40;
  return humi;
}

String readAll() {
  String msg = "";
  float temp = 0;
  float humi = 0;
    
  temp = readTemp();
  String temp_string = String(temp);
  humi = readHumi();
  String humi_string = String(humi);
  msg = "{\"status\":\"success\",\"temperature\":{\"value\":" +temp_string+ ",\"unit\":\"C\"},\"humidity\":{\"value\":" +humi_string+ ",\"unit\":\"%\"}}";

  return msg;
}

