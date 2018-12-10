import sys
import os
import RPi.GPIO as GPIO
import Adafruit_DHT
import time

from pubnub.pubnub import PubNub
from pubnub.pubnub import PNConfiguration

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import apscheduler.events


# configuration

PubNub_Publish_Key = "pub-c-3d630c0e-0ddd-4a02-a07b-cb0c22a5bfcc"
PubNub_Subscribe_Key = "sub-c-df65c840-facc-11e8-9231-4abfa1972993"

pnconf = PNConfiguration()

pnconf.subscribe_key = PubNub_Subscribe_Key
pnconf.publish_key = PubNub_Publish_Key

pubnub = PubNub(pnconf)


# GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4 , GPIO.IN)
GPIO.setup(18 , GPIO.OUT)


def tick():
    print('Tick! The time is %s' % datetime.now)


def killLogger():
    scheduler.shutdown()
    print "Scheduler Shutdown..."
    exit()

def BlinkLED(times , length):

    for i in range(0 , times):
        GPIO.output(4 , 1)
        time.sleep(length)
        GPIO.output(4 , 0)
        time.sleep(length)

def readTemp():
    humidity , temperature = Adafruit_DHT.read_retry(11 , 4)
    print('DHT11 Sensor read at time: %s' % datetime.now())
    print '		Temp:             ' + str(humidity)
    print '		Hum:              ' + str(temperature)

    BlinkLED(2 , 0.200)

    returnValue = []
    returnValue.append(temperature)
    returnValue.append(humidity)

    return returnValue

def publish_callback(result, status):
        print "status.is_error", status.is_error()
        print "status.original_response", status.original_response
        pass


def publishToPubNub():

    hum , temp = Adafruit_DHT.read_retry(11 , 4)
    print('Publishing Data to PubNub time: %s' % datetime.now())
    print '		Temp:             ' + str(temp)
    print '		Hum:              ' + str(hum)
    

    myMessage = {'Temperature': temp, "Humidity": hum}
    pubnub.publish().channel('Temp_Hum').message(myMessage).pn_async(publish_callback)

    BlinkLED(3,0.200)

    returnValue = []
    returnValue.append(tem)
    returnValue.append(hum)

    return returnValue


def ap_my_listener(event):
    if event.exception:
        print event.exception
        print event.traceback

print "---------------"
print "Temp_Hum_PubNub"
print""
print "---------------"


if __name__ == 'main':

    scheduler = BackgroundScheduler()

    scheduler.add_listener(ap_my_listener , apscheduler.events.EVENT_JOB_ERROR)

    # prints out the date and time to console
    scheduler.add_job(tick , 'inteval' , seconds=60)
    # blink life light
    scheduler.add_job(BlinkLED , 'interval' , seconds=5, args = [1 , 0.250])

    # IOT jobs

    scheduler.add_job(readTemp , 'interval', seconds = 10)

    # add the update to pubnub
    scheduler.add_job(publishToPubNub , 'interval' , seconds=2)

    # start scheduler
    scheduler.start()
    print "---------"
    print "Scheduled Jobs"
    print "---------"
    scheduler.print_jobs()
    print "---------"

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))


    
    try:
        	# This is here to simulate application activity (which keeps the main thread alive).
                while True:
                    time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        	# Not strictly necessary if daemonic mode is enabled but should be done if possible
        	scheduler.shutdown












        
