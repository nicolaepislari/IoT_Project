import paho.mqtt.client as mqtt
import json
import cherrypy

class ControlStrategy():

    def __init__(self,reqSoilHum, SoilHumRange=10):
        self.reqSoilHum=reqSoilHum
        self.SoilHumRange=SoilHumRange

    def checkSys(self,realSoilHum):

        if( abs(realSoilHum-realSoilHum) > self.SoilHumRange):
            return True
        else:
            return False

    def action(self):
        # IF checkSys true or Schedule True --> Water
        # ELSE: do nothing
        return


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
    client.subscribe("/section1/soil/humidity")

def on_message(client, userdata, msg):
    content = str(msg.payload)
    d = json.loads(content)



sub = mqtt.Client("WaterControl", False)
sub.on_connect = on_connect
sub.on_message = on_message

sub.connect("192.168.0.102")

sub.loop()
