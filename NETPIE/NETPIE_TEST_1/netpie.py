import microgear.client as microgear
import time
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.IN)
GPIO.setup(3,GPIO.OUT)

appid = "MoMoodyPlantProject"
gearkey = "9Cixu1tG1XachJo"
gearsecret =  "n4ByQyKjHLaqYEekRiYxrQOgV"
ALIAS = "RPi_01"
TARGET_ALIAS = "FreeBoard_01"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)

def disconnect():
    logging.debug("disconnect is work")

microgear.setalias(ALIAS)
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/mails")
microgear.connect(False)
c = 0
while 1:
    if microgear.connected: 
        text_string = "COUNT :" +str(c)
        microgear.chat(ALIAS,text_string)
        logging.debug(">>"+text_string)
    time.sleep(3)
    c+=1