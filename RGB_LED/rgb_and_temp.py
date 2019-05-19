import RPi.GPIO as GPIO
import sys
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
try:
    while True:
          humidity, temperature = Adafruit_DHT.read_retry(11, 7)
          if humidity is not None and temperature is not None:
                #print 'temp = '+ str(temperature)+ str(humidity)
                print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
                if (temperature >= 25 and temperature <= 35 and humidity >= 60):
                    GPIO.output(33,0)
                    GPIO.output(29,1)
                    GPIO.output(31,1)
                else:
                    GPIO.output(33,1)
                    GPIO.output(29,0)
                    GPIO.output(31,0)
                    
          time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()

