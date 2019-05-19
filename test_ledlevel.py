""" https://www.rototron.info/raspberry-pi-analog-water-sensor-tutorial/ """
from time import sleep
import RPi.GPIO as GPIO
import spidev
import sys
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(PUMP_PIN,GPIO.OUT)

PUMP_PIN = 3
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

info = [0,0,0,0]
#[humdity,temp,soil,water_level]
try:
    while True:
        #channel = 0
        info[0],info[1]  = Adafruit_DHT.read_retry(11, 7)
        if info[0] is not None and info[1] is not None:
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(info[1], info[0])
        else:
            print('no value')
        for i in range(0,2):
        # channeldata = poll_sensor(channel)
            channeldata = ReadInput(i)
            info[i+2]=channeldata 
        # voltage = round(((channeldata * 3300) / 1024), 0)
        # print('Voltage (mV): {}'.format(voltage))
            print('Data{} : {}\n'.format(i,channeldata))

        # if voltage < 50:
        #     # Green
        #     print("GREEN")
        # elif voltage < 1800:
        #     # Yellow
        #     print("YELLOW")
        # else:
        #     # Red
        #     print("RED")
            sleep(1)
        
        if (info[1] >= 25 and info[1] <= 35 and info[0] >= 50 and info[2]<500 and info[2]>300):
            #default level
            print('default')
            GPIO.output(33,0)
            GPIO.output(29,1)
            GPIO.output(31,0)
        elif info[2]<=300 :
            #good 
            print('watering')
            GPIO.output(33,0)
            GPIO.output(29,1)
            GPIO.output(31,1)
        else:
            #not good
            #water pump active
            for i in range(0,2):
                GPIO.output(PUMP_PIN,GPIO.HIGH)
                print('pump active')
                time.sleep(3)
            print('hungry')
            GPIO.output(33,1)
            GPIO.output(29,0)
            GPIO.output(31,1)

        if(info[3]<=200):
            #warning
            print('no water')
finally:                # run on exit
    spi.close()         # clean up
    GPIO.cleanup()
    print "\n All cleaned up."