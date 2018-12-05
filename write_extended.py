#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import mysql.connector
import cv2
import os


def get_face_data(face_tag):
	cam = cv2.VideoCapture(0)
	cam.set(3, 640) # set video width
	cam.set(4, 480) # set video height

	face_detector = cv2.CascadeClassifier('/root/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml')

	# For each person, enter one numeric face id
	face_id = face_tag

	print("\n [INFO] Initializing face capture. Look the camera and wait ...")
	# Initialize individual sampling face count
	count = 0

	while(True):

    		ret, img = cam.read()
   		# img = cv2.flip(img, -1) # flip video image vertically
    		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    		faces = face_detector.detectMultiScale(gray, 1.3, 5)

    		for (x,y,w,h) in faces:

        		cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        		roi_gray = gray[y:y+h, x:x+w]
        		roi_color = img[y:y+h, x:x+w]
        		count += 1

       			# Save the captured image into the datasets folder
        		cv2.imwrite("/root/face_db/dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        		cv2.imshow('image', img)

    		k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    		if k == 27:
        		break
    		elif count >= 30: # Take 30 face sample and stop video
         		break

	# Do a bit of cleanup
	print("\n [INFO] Exiting Program and cleanup stuff")
	cam.release()
	cv2.destroyAllWindows()



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
	return mycursor.lastrowid





reader = SimpleMFRC522.SimpleMFRC522()

try:
        name = raw_input('Person Name:')
	attending_class = raw_input('Class Name:')
	print('Entering Data to the database....')
	data_id = update_db(name, attending_class)

	if data_id > 0 :
		print('Capturing Facial data....')
		get_face_data(data_id)
		print("Now place your tag to write....")
        	reader.write(str(data_id))
        	print("Written")
finally:
        GPIO.cleanup()

