import microgear.client as microgear
import time
import logging

appid = "freeboardIN"
gearkey = "lS7eJDIjF08pvmM"
gearsecret =  "GvnWEm51u3vg8hFzogkkQZZRO"

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
#microgear.subscribe("/ldr")
microgear.connect(False)

count = 0
while True:
    if(microgear.connected):
        microgear.publish("/ldr", str(count))
        print count
        count = count + 10
    time.sleep(1)

