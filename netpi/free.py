import microgear.client as microgear
import time
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.IN)
GPIO.setup(11,GPIO.OUT)

appid = "freeboardIN"
gearkey = "lM2hhvEEvOIh8HW"
gearsecret =  "c7whwsOCZnZ2PRYzSLVhJ3Fri"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    #logging.info(topic+" "+message)
    #print message
    global s
    if message == "ON":
        if (s == 1):
            s = 0
            GPIO.output(11,GPIO.LOW)
            #time.sleep(0.5)
        elif (s == 0):
            s=1
            GPIO.output(11,GPIO.HIGH)
            #time.sleep(0.5)
    logging.info(topic+"-- "+str(s))
    microgear.publish("/ldr", str(s))
        

def disconnect():
    logging.debug("disconnect is work")

s = 0
microgear.setalias("Pi")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect                                                                                                                                                                                                                                                                                                                                                                                               
microgear.subscribe("/ldr")
microgear.connect(False)


while True:
    #if(microgear.connected):
        time.sleep(2)

