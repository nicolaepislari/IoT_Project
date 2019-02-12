\import Adafruit_DHT
import time
import json

class DHT_Read():
	""" Read Temperature and Humidity """

	def __init__(self):
		self.humidity = None
		self.temp     = None
		self.sensor   = Adafruit_DHT.DHT11

	def read(self):
		try:
			self.humidity, self.temp = Adafruit_DHT.read_retry(self.sensor, 17)
		except:
			print "Error in reading from Sensor"

		if(self.humidity is not None and self.temp is not None):
			
			json_file=json.dumps({"temperature":self.temp, "humidity": self.humidity, "time": time.time()})
			
			return json_file			
	
