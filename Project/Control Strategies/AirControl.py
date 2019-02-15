import paho.mqtt.client as mqtt
import json
import requests

class AirControl():

    def __init__(self, minH, maxH ,maxT, minT, zoneID, catalogIP):
        self.minH = minH
        self.maxH = maxH
        self.minT = minT
        self.maxT = maxT
        self.zone = zoneID
        self.url = catalogIP



        respond = requests.get(url)
    def checkSys(self, realTemp,realHum):
        if(realTemp >= self.maxT):
            print "Temperature too high"
            userList = json.loads(requests.get(self.url + "/users").text)
            for i in userList:

                if i["emergency"]==True:
                    url="https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+str(i['chat_id'])\
                        +"&text=Temperature too high in ZONE "+self.zone[-1]+". Turing on cooling system!"
                    requests.post(url)

Emergency = True
broker="192.168.0.100"
token = "780431995:AAFHKfKwhC31k23iYY4P96a7sXjZb8U4Dog"
chat_id = [522064827]