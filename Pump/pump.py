
import RPi.GPIO as GPIO
import time

PUMP_PIN =  3

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PUMP_PIN,GPIO.OUT)

while(1):
    
    GPIO.output(PUMP_PIN,0)
    print("ON")
    time.sleep(3)
    GPIO.output(PUMP_PIN,1)
    print("OFF")
    time.sleep(3)