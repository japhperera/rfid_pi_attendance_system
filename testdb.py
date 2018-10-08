#!/usr/bin/env python

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="pi",
  passwd="pi@123",
 database="AT_SYS"
)

mycursor = mydb.cursor()

#create_query = "CREATE TABLE students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),tag VARCHAR(255))"
create_query = "CREATE TABLE attendance (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),tag VARCHAR(255),date VARCHAR(20), time VARCHAR(10))"

mycursor.execute(create_query)

for x in mycursor:
  print(x)

