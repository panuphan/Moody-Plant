#!/usr/bin/python
import sys
import Adafruit_DHT
import time
while True:
  humidity, temperature = Adafruit_DHT.read_retry(11, 8)
  if humidity is not None and temperature is not None:
    print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
  else:
    print 'Failed to get reading. Try again!'
  time.sleep(1)