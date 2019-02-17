#!/usr/bin/env python
import cayenne.client
import json
from threading import Thread
import requests

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../catalog/')))
from util import *

import cherrypy
import time
import datetime


# Cayenne virtual board
MQTT_USERNAME  = "d9d7b3d0-6274-11e7-8c3a-27ab5d31c1f7"
MQTT_PASSWORD  = "55053331506ab1ece82c1e855cbb473bb84f2980"
MQTT_CLIENT_ID = "da2db570-2e54-11e9-a056-c5cffe7f75f9"


# Cayenne interface
# MQTT_USERNAME  = "dfa82ba0-59e6-11e7-9c17-adc0b1d0cf53"
# MQTT_PASSWORD  = "e7cac152da7188253698f47018410a88e17d498f"
# MQTT_CLIENT_ID = "739655a0-bc5e-11e8-a79e-89b0eb263992"

headers = {'content-type': 'application/json'}



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





class adaptorWS():
    exposed= True

    def GET(self,*uri,**params):
        if not uri:
            return "not URI"
        if uri[0] == 'print_adaptor':
            return "print_adaptor"
        


    def POST(self,*uri,**params):
        '''
            The method is used to update the information in the catalog.json file
        '''
        # reads the BODY content of the POST Method
        body_payload = cherrypy.request.body.read()
        print ("body_payload = %s" %body_payload)
        print ("type = %s" %type(body_payload.decode("utf-8") ))
        new_data_dict = json.loads(body_payload.decode("utf-8") )


        if not uri:
            # reads the BODY content of the POST Method
            body_payload = cherrypy.request.body.read()
            print ("body_payload = %s" %body_payload)
      


        elif uri[0] == "iamalive":
            '''
                check the actors in the catalog file and register/update them 
                with the current time and date
            '''
        
            actor_dict = old_catalog_dict['actor']


            return ("I am alive")

        elif uri[0] == "removeme":
            return ("removeme")

            
class Cayenne_routine(Thread):

    def __init__(self, MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID):


        Thread.__init__(self)
        self.daemon = True
        self.MQTT_USERNAME = MQTT_USERNAME
        self.MQTT_PASSWORD = MQTT_PASSWORD
        self.MQTT_CLIENT_ID = MQTT_CLIENT_ID
        self.start()


    def run(self):
        
        ###################################### CAyenne MQTT routine
        client = cayenne.client.CayenneMQTTClient()
        client.on_message = on_message
        client.begin(self.MQTT_USERNAME, self.MQTT_PASSWORD, self.MQTT_CLIENT_ID)
        # For a secure connection use port 8883 when calling client.begin:
        # client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883)
        client.loop_forever()
        #######################################




if __name__ == '__main__':


    Cayenne_routine(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)



    file_conf=open('conf.json','r')
    adaptor_conf=json.load(file_conf)

    host = adaptor_conf['host']
    port = adaptor_conf['port']
    file_conf.close()
    
    
    # configurations for cherrypy
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }
    
    #creating a thread to remove actors that are older than 60 sec
    # Actor_removal(catalog_name, time_to_live)

    cherrypy.server.socket_host = host
    cherrypy.server.socket_port = port
    cherrypy.tree.mount (adaptorWS(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()




