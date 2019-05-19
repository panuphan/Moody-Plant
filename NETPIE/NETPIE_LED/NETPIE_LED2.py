import microgear.client as microgear
import time
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.IN)
GPIO.setup(11,GPIO.OUT)

appid = "MyFirstNETPIE"
gearkey = "GkTghcqVrGLuP4v"
gearsecret =  "2N0e46vfAK0WG5ljyLid42x0R"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)
    print message
    if message == "ON":
        GPIO.output(11,GPIO.HIGH)
        microgear.chat("HTML_web", "ON")
    else:
        GPIO.output(11,GPIO.LOW)
        microgear.chat("HTML_web", "OFF")

def disconnect():
    logging.debug("disconnect is work")

microgear.setalias("Pi")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect                                                                                                                                                                                                                                                                                                                                                                                               
microgear.subscribe("/mails")
microgear.connect(False)

while True:
    if(microgear.connected):
        time.sleep(0.2)

