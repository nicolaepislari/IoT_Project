import paho.mqtt.client as mqtt
import json
import cherrypy

class ControlStrategy():
    def __init__(self, reqTemp,reqHum,TempRange = 5, HumidityRange = 5):
        self.reqTemp=reqTemp
        self.reqHum=reqHum
        self.TempRange=TempRange
        self.HumidityRange=HumidityRange
    def checkSys(self, realTemp,realHum):
        if (abs(realTemp-self.reqTemp)> self.TempRange):

            if( abs(realHum-self.reqHum) > self.HumidityRange):

                #Activate Ventilation
                print("Temp and Hum out of Range")

            else:
                print("Only Temp out of range")

            if (abs(realHum - self.reqHum) > 2*self.HumidityRange):
                print("Temperature Difference Very High")
                print("Send warning")

class WebControl():
    exposed=True
    def GET(self,*uri,**par):
        return False
    def POST(self, *uri, **par):
        return True
    def PUT(self, *uri, **par):
        return True
    def DEL(self, *uri, **par):
        return True



def on_connect(client, userdata, flags, rc):
    client.subscribe("/section1/temp")
    client.subscribe("/section1/humidity")

def on_message(client, userdata, msg):
    content = str(msg.payload)
    d = json.loads(content)



sub = mqtt.Client("AirControlTemp", False)
sub.on_connect = on_connect
sub.on_message = on_message

sub.connect("192.168.0.102")

sub.loop()
