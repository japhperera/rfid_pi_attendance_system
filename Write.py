#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import mysql.connector

def update_db(name, tag):
	mydb = mysql.connector.connect(
 			host="localhost",
  			user="pi",
  			passwd="pi@123",
 			database="AT_SYS"
	)

	mycursor = mydb.cursor()
	insert_query = "INSERT INTO students (name, tag) VALUES (%s, %s)"	
	val = (name, tag)

	mycursor.execute(insert_query,val)
	mydb.commit()
	print("1 record inserted, ID:", mycursor.lastrowid)




reader = SimpleMFRC522.SimpleMFRC522()

try:
        text = raw_input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
	update_db(text, "New Student")
finally:
        GPIO.cleanup()
