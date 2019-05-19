import microgear.client as microgear
import time
import logging
import RPi.GPIO as GPIO
import sys
from time import sleep
import spidev
import Adafruit_DHT

GPIO.setwarnings(False)
PUMP_PIN = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(PUMP_PIN,GPIO.OUT)

appid = "MoodyPlant"
gearkey = "4vAN246i0mJ6Del"
gearsecret =  "x2zcDw1cctrJKvZFm86tUsAI3"

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 250000

def poll_sensor(channel):
        """Poll MCP3002 ADC
        Args:
            channel (int):  ADC channel 0 or 1
        Returns:
            int: 10 bit value relating voltage 0 to 1023
        """
        assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'

        # First bit of cbyte is single=1 or diff=0.
        # Second bit is channel 0 or 1
        if channel:
            cbyte = 0b11000000
        else:
            cbyte = 0b10000000

        # Send (Start bit=1, cbyte=sgl/diff & odd/sign & MSBF = 0)
        r = spi.xfer2([1, cbyte, 0])

        # 10 bit value from returned bytes (bits 13-22):
        # XXXXXXXX, XXXX####, ######XX
        return ((r[1] & 31) << 6) + (r[2] >> 2)

#Read SPI Sensor input 0 to 7 for MCP3008
def ReadInput(Sensor):
    adc = spi.xfer2([1,(8+Sensor)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data


#mood plant
def getmood(num):
    if (num==0):
        return "HAPPY"
    elif(num==1):
        return "WATERING"
    elif(num==2):
        return "I'M HUNGRY"

microgear.setalias("Pi")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect                                                                                                                                                                                                                                                                                                                                                                                               
#microgear.subscribe("/ldr")
microgear.connect(False)

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    print message
    global status
    if message == "ON":
        GPIO.output(PUMP_PIN,GPIO.HIGH)
        status = "ON"
    else :
        GPIO.output(PUMP_PIN,GPIO.LOW)
        status = "OFF"

    logging.info(topic+"-- "+status)
    microgear.publish("/gearname/ldr", status)
        
def disconnect():
    logging.debug("disconnect is work")

sensor = ""
status = "OFF"#status_pump
try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 7)
        if temperature is not None and humidity is not None:
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        sensor = str(humidity)+','+str(temperature)
        soil = ReadInput(0)
        waterlevel = ReadInput(1)
        print 'soil ='+str(soil)
        print 'waterlevel ='+str(waterlevel)
        mood = ""
        water = ""
        if(waterlevel<=200):
            #warning
            water = 0
            print('no water')
            GPIO.output(33,1)
            GPIO.output(29,0)
            GPIO.output(31,0)

        if (temperature >= 25 and temperature <= 35 and humidity >= 50 and soil<500 and soil>300):
            #default level
            mood = getmood(0)
            GPIO.output(33,0)
            GPIO.output(29,1)
            GPIO.output(31,0)
        elif soil<=300 :
            #good 
            mood = getmood(1)
            #print('watering')
            GPIO.output(33,0)
            GPIO.output(29,1)
            GPIO.output(31,1)
        else:
            #not good
            #water pump active
            mood = getmood(2)
            #print('hungry')
            GPIO.output(33,1)
            GPIO.output(29,0)
            GPIO.output(31,1)
            GPIO.output(PUMP_PIN,GPIO.HIGH)
            status = 1
            #print('pump active')
            print('watering')
            microgear.chat("/ldr",sensor)
            time.sleep(5)
            GPIO.output(33,0)
            GPIO.output(29,1)
            time.sleep(1)
            GPIO.output(PUMP_PIN,GPIO.LOW)
            status = 0

        sensor = str(humidity)+','+str(temperature)+','+str((soil-200)*0.222)+','+str(waterlevel*0.285)+','+status+','+mood
        #time.sleep(0.3)
        if(microgear.connected):
            print sensor
            microgear.chat("/ldr",sensor)
            
        time.sleep(0.3)
finally:                # run on exit
    spi.close()         # clean up
    GPIO.cleanup()
    print "\n All cleaned up."