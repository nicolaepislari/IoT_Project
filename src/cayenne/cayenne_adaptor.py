#!/usr/bin/env python
import cayenne.client
import json
import requests
# Cayenne virtual board
MQTT_USERNAME  = "d9d7b3d0-6274-11e7-8c3a-27ab5d31c1f7"
MQTT_PASSWORD  = "55053331506ab1ece82c1e855cbb473bb84f2980"
MQTT_CLIENT_ID = "da2db570-2e54-11e9-a056-c5cffe7f75f9"


# Cayenne interface
# MQTT_USERNAME  = "dfa82ba0-59e6-11e7-9c17-adc0b1d0cf53"
# MQTT_PASSWORD  = "e7cac152da7188253698f47018410a88e17d498f"
# MQTT_CLIENT_ID = "739655a0-bc5e-11e8-a79e-89b0eb263992"

headers = {'content-type': 'application/json'}

url_b1 = 'http://192.168.43.154/cmd'
payload1_on = {'leds': 'on'}
payload1_off = {'leds': 'off'}

url_b11_on = "http://192.168.43.154/leds/1/on"
url_b11_off = "http://192.168.43.154/leds/1/off"

url_b12_on = "http://192.168.43.154/leds/2/on"
url_b12_off = "http://192.168.43.154/leds/2/off"

url_b2 = 'http://192.168.43.127/cmd'
payload2_on = {'leds': 'on'}
payload2_off = {'leds': 'off'}

url_b21_on = "http://192.168.43.127/leds/1/on"
url_b21_off = "http://192.168.43.127/leds/1/off"

url_b22_on = "http://192.168.43.127/leds/2/on"
url_b22_off = "http://192.168.43.127/leds/2/off"
# The callback for when a message is received from Cayenne.
def on_message(message):
    print("message received: " + str(message))   
    # If there is an error processing the message return an error string, otherwise return nothing.
    channel = message.channel
    value = int(message.value)
    
    print (channel)
    print (value)


    # if channel == 2:
    #   print("channel = %s" %channel)
    #   print("value = %s" %value)
    #   if value == 1:
    #     ON()
    #   if value == 0:
    #     OFF()



 
def b1_on():
  print("b1_on")
  r = requests.post(url_b1, data=json.dumps(payload1_on), headers=headers)
  print ("POST %s -> %s" %(url_b1, payload1_on))

def b1_off():
  print("b1_off")
  r = requests.post(url_b1, data=json.dumps(payload1_off), headers=headers)
  print ("POST %s -> %s" %(url_b1, payload1_off))


def b2_on():
  print("b2_on")
  r = requests.post(url_b2, data=json.dumps(payload2_on), headers=headers)
  print ("POST %s -> %s" %(url_b2, payload1_on))






client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883)
client.loop_forever()