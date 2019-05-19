import microgear.client as microgear
import time
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.IN)
GPIO.setup(3,GPIO.OUT)

appid = "MoodyPlantProject"
gearkey = "9Cixu1tG1XachJo"
gearsecret =  "n4ByQyKjHLaqYEekRiYxrQOgV"
ALIAS = "RPi_01"
TARGET_ALIAS = "FreeBoard_01"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)
    global sw
    if(message == "switch"):
	sw=(sw+1)%2
	print("SW")

def disconnect():
    logging.debug("disconnect is work")

microgear.setalias(ALIAS)
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
#microgear.subscribe("/mails")
microgear.connect(False)
c = 0
c2= 5

sw = 0

while 1:
    if(microgear.connected): 
        text_string = "COUNT :" +str(c)
        #microgear.chat(ALIAS,text_string)
        print(">>"+text_string)
	text_2 = "NO.2:"+str(c2)
	print(">>"+text_2)
	print(">>"+str(sw))
        microgear.chat(TARGET_ALIAS,text_string+";"+text_2+';'+str(sw))
    time.sleep(3)
    c+=1
    c2+=3
