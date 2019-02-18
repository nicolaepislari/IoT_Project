#!/usr/bin/env python
import cayenne.client
import json
import requests
import time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "d9d7b3d0-6274-11e7-8c3a-27ab5d31c1f7"
MQTT_PASSWORD  = "55053331506ab1ece82c1e855cbb473bb84f2980"
MQTT_CLIENT_ID = "da2db570-2e54-11e9-a056-c5cffe7f75f9"

client = cayenne.client.CayenneMQTTClient()

client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)
##################################################################################




headers = {'content-type': 'application/json'}

url_b1 = 'http://192.168.1.13'


read_uri = '/read'
payload_temp = {'read': 'temp'}
payload_humi = {'read': 'humi'}
payload_all = {'read': 'all'}

waterpump_uri = '/waterpump'
payload_pump_on = {'waterpump': 'on'}
payload_pump_off = {'waterpump': 'off'}
payload_pump_state = {'waterpump': 'state'}

fan_uri = '/fan'
payload_fan_on = {'fan': 'on'}
payload_fan_off = {'fan': 'off'}
payload_fan_state = {'fan': 'state'}


# def read_temp():
#   print ("POST %s -> %s" %(url_b1, payload_temp))
#   r = requests.post(url_b1, data=json.dumps(payload_temp), headers=headers)
#   logger.info("Response from esp: %s" % r.content)

# def read_humi():
#   print ("POST %s -> %s" %(url_b1, payload_humi))
#   r = requests.post(url_b1, data=json.dumps(payload_humi), headers=headers)
#   logger.info("Response from esp: %s" % r.content)

def read_all():
  print ("POST %s -> %s" %(url_b1 + read_uri, payload_all))
  r = requests.post(url_b1 + read_uri, data=json.dumps(payload_all), headers=headers)
  # logger.info("Response from esp: %s" % r.content)
  print(r.content)
  return json.loads(r.content.decode("utf-8"))

def send_temp_to_cayenne(channel, data):
  client.virtualWrite(channel, data) #Publish "1" to Cayenne MQTT Broker Channel 3
  # print("Button pressed\n")

def send_humi_to_cayenne(channel, data):
  client.virtualWrite(channel, data) #Publish "0" to Cayenne MQTT Broker Channel 3
  # print("Button released\n")


def send_to_thingspeak(temp, humi):
  #https://api.thingspeak.com/update?api_key=KD8ASSYPPCNQ709V&field1=0
  ts_url = "https://api.thingspeak.com/update.json"
  thSPK_API_KEY = "KD8ASSYPPCNQ709V"
  ts_channel_id = "705897"
  temp_field = 1
  humi_field = 2

  headers = {'content-type': 'application/json'}
  payload = {'api_key': thSPK_API_KEY, 'channel_id': ts_channel_id, "field1": temp,
              "field2": humi}

  r = requests.post(ts_url, data=json.dumps(payload), headers=headers)
  print (r.content)


def control_fan(payload):
  # url_b1  = 'http://192.168.1.13'
  # fan_uri = '/fan'
  # request to 'http://192.168.1.13/fan' 

  print ("POST %s -> %s" %(url_b1 + fan_uri, payload))
  r = requests.post(url_b1 + fan_uri, data=json.dumps(payload), headers=headers)
  # logger.info("Response from esp: %s" % r.content)
  print(r.content)
  return json.loads(r.content.decode("utf-8"))

def control_pump(payload):
  # url_b1  = 'http://192.168.1.13'
  # fan_uri = '/waterpump'
  # request to 'http://192.168.1.13/waterpump' 

  print ("POST %s -> %s" %(url_b1 + waterpump_uri, payload))
  r = requests.post(url_b1 + waterpump_uri, data=json.dumps(payload), headers=headers)
  # logger.info("Response from esp: %s" % r.content)
  print(r.content)
  return json.loads(r.content.decode("utf-8"))

while True:
  # client.loop()

  # response = read_all()
  # print(response)
  # if response['status'] == "success":
  #   temperature = response['temperature']
  #   humidity = response['humidity']
  #   # print("temperature: " + str(temperature))
  #   # print("humidity: " + str(humidity))

  #   send_temp_to_cayenne(1,"temp,c=20.7")
  #   send_humi_to_cayenne(2,humidity['value'])


  #   send_temp_to_cayenne(21, temperature['value'])
  #   send_humi_to_cayenne(22,humidity['value'])

  #   send_to_thingspeak(temperature['value'], humidity['value'])

  # else:
  #   print("ERRRRRRRRRRRRRRRR")
  #   print(response['message'])
  # print("\n")

  control_pump(payload_pump_on)
  time.sleep(1)

  control_pump(payload_pump_off)
  time.sleep(1)

  control_pump(payload_pump_state)
  time.sleep(1)
  print ()
  
  control_fan(payload_fan_on)
  time.sleep(1)
  
  myvar = control_fan(payload_fan_off)
  print(myvar)
  time.sleep(1)
  
  control_fan(payload_fan_state)
  time.sleep(1)
  print ()




# # The callback for when a message is received from Cayenne.
# def on_message(message):
#     print("message received: " + str(message))   
#     # If there is an error processing the message return an error string, otherwise return nothing.
#     channel = message.channel
#     value = int(message.value)
    
#     print (type(channel))
#     print (type(value))


#     if channel == 2:
#       print("channel = %s" %channel)
#       print("value = %s" %value)
#       if value == 1:
#         ON()
#       if value == 0:
#         OFF()

# def b1_on():
#   print("b1_on")
#   r = requests.post(url_b1, data=json.dumps(payload1_on), headers=headers)
#   print ("POST %s -> %s" %(url_b1, payload1_on))

# def b1_off():
#   print("b1_off")
#   r = requests.post(url_b1, data=json.dumps(payload1_off), headers=headers)
#   print ("POST %s -> %s" %(url_b1, payload1_off))


# client = cayenne.client.CayenneMQTTClient()
# client.on_message = on_message
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)
# # For a secure connection use port 8883 when calling client.begin:
# # client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883)
# client.loop_forever()