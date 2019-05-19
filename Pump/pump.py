
import RPi.GPIO as GPIO
import time

PUMP_PIN =  3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PUMP_PIN,GPIO.OUT)

try:
    while(1):
        
        GPIO.output(PUMP_PIN,GPIO.HIGH)
        print("ON")
        time.sleep(3)
        GPIO.output(PUMP_PIN,GPIO.LOW)
        print("OFF")
        time.sleep(3)
except:
    print("Cleanup")
    GPIO.cleanup()