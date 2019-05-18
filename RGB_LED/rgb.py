import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23,0)
GPIO.setup(35, GPIO.OUT)
GPIO.output(35,0)
GPIO.setup(33, GPIO.OUT)
GPIO.output(33,0)

try:
	while(True):
    		request = raw_input("RGB-->")
    		if(len(request)==3):
                    print request[0]
                    GPIO.output(23,int(request[0]))
                    GPIO.output(33,int(request[1]))
                    GPIO.output(35,int(request[2]))
except KeyboardInterrupt:
	GPIO.cleanup()
