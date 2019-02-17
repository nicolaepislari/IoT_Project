import cayenne.client #Cayenne MQTT Client 
from time import sleep




# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "d9d7b3d0-6274-11e7-8c3a-27ab5d31c1f7"
MQTT_PASSWORD  = "55053331506ab1ece82c1e855cbb473bb84f2980"
MQTT_CLIENT_ID = "da2db570-2e54-11e9-a056-c5cffe7f75f9"

client = cayenne.client.CayenneMQTTClient()

client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

def send_on(x):
  client.virtualWrite(1, x) #Publish "1" to Cayenne MQTT Broker Channel 3
  print("Button pressed\n")

def send_off(x):
  client.virtualWrite(1, x) #Publish "0" to Cayenne MQTT Broker Channel 3
  print("Button released\n")

  
while True:
  client.loop()
  for i in range(10):
      print (i)
      send_on(i)
      sleep(1)
      send_off(i*2)
      sleep(1)