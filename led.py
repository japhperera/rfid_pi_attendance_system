import RPi.GPIO as GPIO 
import time
 
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(18,GPIO.OUT)

while True:
	print"LED on"
	GPIO.output(18,GPIO.HIGH)
	time.sleep(2)
	print "LED 0ff"
	GPIO.output(18,GPIO.LOW)
	time.sleep(2)
