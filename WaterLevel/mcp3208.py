from mcp3208 import MCP3208
import RPi.GPIO as GPIO
import time

pwmPin = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(3,GPIO.OUT)
pwm1 = GPIO.PWM(pwmPin,120) #PWM frequency
pwm1.start(0)
adc = MCP3208()

while(1):
    print(adc.read(0))
    pwm1.ChangeDutyCycle(adc.read(0)/40.95)
    time.sleep(0.5)