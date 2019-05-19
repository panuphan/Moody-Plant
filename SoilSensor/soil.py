from mcp3208 import MCP3208
import RPi.GPIO as GPIO
import time

SOIL_PIN =  3

# pwmPin = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(SOIL_PIN,GPIO.IN)


# GPIO.setup(3,GPIO.OUT)
# pwm1 = GPIO.PWM(pwmPin,120) #PWM frequency
# pwm1.start(0)

adc = MCP3208()

def callback(PIN):
    if GPIO.input(PIN):
        print("No Water")
    else:
        print("Water !!")

GPIO.add_event_detect(SOIL_PIN,GPIO.BOTH,bouncetime=300)
GPIO.add_event_callback(SOIL_PIN,callback)

while(1):
    soil_sensor = adc.read(0)
    print("Soil>>"+soil_sensor)
    # pwm1.ChangeDutyCycle(adc.read(0)/40.95)
    # pwm1.ChangeDutyCycle(adc.read(0))
    # print(">>"+str(GPIO.input(pwmPin)))
    time.sleep(0.5)