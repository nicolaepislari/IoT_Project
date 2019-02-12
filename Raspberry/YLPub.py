from YL69 import YL_Read
import paho.mqtt.client as mqtt
import json
import time

class YL_Pub:
	
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
updateTime = 5

sensor = YL_Read(17)


publisher = YL_Pub("YL69", broker)
publisher.start()

while True:

	val=sensor.readAvg() 
	if val[0]=='{':
		jsonDic=json.loads(val)
		print jsonDic
		
		#Publish Moisture
		temp='{"moisture": ' + str(jsonDic["moisture"])+', "time": '+str(jsonDic["time"])+'}'
		publisher.publish("/zone1/soil/moisture",temp) 
			
	else:
		print "Error reading from sensor"
	time.sleep(updateTime)
