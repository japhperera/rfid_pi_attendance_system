#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import time
import mysql.connector
import datetime
import cv2
import numpy as np
import os 



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



def get_data_from_db(id):
	
	mydb = mysql.connector.connect(
                        host="localhost",
                        user="pi",
                        passwd="pi@123",
                        database="AT_SYS"
        )
	mycursor = mydb.cursor()
        select_query = """select * from students where id = %s"""
	mycursor.execute(select_query,(id,))
        myresult = mycursor.fetchall()
	for row in myresult:
            print("Id = ", row[0], )
            print("Name = ", row[1])
            print("Class = ", row[2])
	return myresult



           
def recognize(tag_id, tag_name):
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('/root/face_db/trainer/trainer.yml')
	cascadePath = "/root/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascadePath);

	font = cv2.FONT_HERSHEY_SIMPLEX

	#iniciate id counter
	id = 0
	# names related to ids: example ==> Marcelo: id=1,  etc
	#names = ['None', 'Pubudu', 'Shaki', 'Ilza', 'Z', 'W'] 

	# Initialize and start realtime video capture
	cam = cv2.VideoCapture(0)
	cam.set(3, 640) # set video widht
	cam.set(4, 480) # set video height

	# Define min window size to be recognized as a face
	minW = 0.1*cam.get(3)
	minH = 0.1*cam.get(4)
	
	match_count=0

	
	for x in range(100):

    		ret, img =cam.read()
   		# img = cv2.flip(img, -1) # Flip vertically

    		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    		faces = faceCascade.detectMultiScale( 
                            gray,
                            scaleFactor = 1.2,
                            minNeighbors = 5,
                            minSize = (int(minW), int(minH)),
       			)

    		for(x,y,w,h) in faces:

                            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                            # Check if confidence is less them 100 ==> "0" is perfect match :
                            if (confidence < 50) and ( id == tag_id):
                                id = tag_id
                                confidence = "  {0}%".format(round(100 - confidence))
                                match_count  = match_count+1
                            else:
                                id = "unknown"
                                confidence = "  {0}%".format(round(100 - confidence))
        
                            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
   		cv2.imshow('camera',img)
   		k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                if k == 27:
                    break
   	    
	# Do a bit of cleanup
	print("\n [INFO] Exiting from recognizer")
	cam.release()
	cv2.destroyAllWindows()
	return match_count

	

def authenticate(reader):
	id, text = reader.read()
	record = get_data_from_db(text)
	
	id = 0
	name=""
	at_class=""
	for row in record:
            id =  row[0]
            name = row[1]
            at_class = row[2]

        match_count = recognize(id, name)
        if match_count > 50:
            print ("Face Ditection Success ... :) ")
            update_db(name,id)
        else:
            print ("Face Ditection Failed !!!!")



reader = SimpleMFRC522.SimpleMFRC522()
while True:
	print ("Waiting for a tag ....")
	authenticate(reader)
