#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import time 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

def blink_led():
	GPIO.output(18,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(18,GPIO.LOW)


def get_data():
        id, text = reader.read()
        print(id)
        print(text)
	blink_led()




reader = SimpleMFRC522.SimpleMFRC522()
while True:
	print "Waiting for a tag ...."
	get_data()
rr
