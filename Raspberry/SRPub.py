from SR04 import SR_Read
import paho.mqtt.client as mqtt
import json
import time

class SR_Pub:
	
	def __init__(self, clientID, broker):
		
		self.clientID = clientID		
		self.pub=mqtt.Client(self.clientID)
		self.broker = broker
	
	def start(self):

		self.pub.connect(broker)
		self.pub.loop_start()

	def stop(self):
		
		self.pub.loop_stop()
		self.pub.disconnect()
	
	def publish(self, topic, message):
		
		self.pub.publish(topic, message)


broker = '192.168.0.100'
ID = "zone1"
updateTime = 1

sensor = SR_Read()


publisher = SR_Pub("SR04", broker)
publisher.start()

while True:

	val=sensor.read() 
	if val[0]=='{':
		jsonDic=json.loads(val)
		print jsonDic
		
		#Publish Tank Level
		temp='{"level": ' + str(jsonDic["level"])+', "time": '+str(jsonDic["time"])+'}'
		publisher.publish("/zone1/water/level",temp) 
			
	else:
		print "Error reading from sensor"
	time.sleep(updateTime)
