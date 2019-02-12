from DHT import DHT_Read
import paho.mqtt.client as mqtt
import json

class DHT_Pub:
	
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

sensor = DHT_Read()


publisher = DHT_Pub("DHT11", broker)
publisher.start()

while True:

	val=sensor.read() 
	if val[0]=='{':
		jsonDic=json.loads(val)
		#print jsonDic
		
		#Publish Temperature
		temp='{"temperature": ' + str(jsonDic["temperature"])+', "time": '+str(jsonDic["time"])+'}'
		publisher.publish("/zone1/air/temp",temp) 
		
		#Publish Humidity
		hum='{"humidity": ' + str(jsonDic["humidity"])+', "time": '+str(jsonDic["time"])+'}'
		publisher.publish("/zone1/air/humidity",hum) 
			
	else:
		print "Error reading from sensor"
