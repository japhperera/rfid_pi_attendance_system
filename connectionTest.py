#!/usr/bin/env python

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="pi",
  passwd="pi@123"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)


