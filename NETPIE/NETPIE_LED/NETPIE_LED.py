import microgear.client as microgear
import time
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.IN)
GPIO.setup(3,GPIO.OUT)

appid = "MyFirstNETPIE"
gearkey = "GkTghcqVrGLuP4v"
gearsecret =  "2N0e46vfAK0WG5ljyLid42x0R"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)

def disconnect():
    logging.debug("disconnect is work")

microgear.setalias("Pi")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/mails")
microgear.connect(False)

status = "OFF"
while True:
    if(microgear.connected):
        if(GPIO.input(5)==0):
            if status == "OFF":
                GPIO.output(3,GPIO.HIGH)
                status = "ON"
                microgear.chat("HTML_web", status)
            else:
                GPIO.output(3,GPIO.LOW)
                status = "OFF"
                microgear.chat("HTML_web", status)
    time.sleep(0.2)

