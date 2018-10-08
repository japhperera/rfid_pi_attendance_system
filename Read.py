#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import time
import mysql.connector
import datetime

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
	update_db(text, id)
	blink_led()


def update_db(name, tag):
	mydb = mysql.connector.connect(
 			host="localhost",
  			user="pi",
  			passwd="pi@123",
 			database="AT_SYS"
	)

	mycursor = mydb.cursor()
	insert_query = "INSERT INTO attendance (name, tag,date,time) VALUES (%s, %s,%s, %s)"
	now = datetime.datetime.now()
	cr_date = now.strftime("%Y-%m-%d")
	cr_time = now.strftime("%H:%M")	
	val = (name, tag, cr_date, cr_time )

	mycursor.execute(insert_query,val)
	mydb.commit()
	print("1 record inserted, ID:", mycursor.lastrowid)






reader = SimpleMFRC522.SimpleMFRC522()
while True:
	print "Waiting for a tag ...."
	get_data()






