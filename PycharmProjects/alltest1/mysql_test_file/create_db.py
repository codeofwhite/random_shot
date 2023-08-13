import mysql.connector

connection = mysql.connector.connect(host='localhost', port='3307', user='root', password='Jason20040903')

cursor = connection.cursor()
# cursor.execute('create database `qq`;')  # sql指令

cursor.execute('show databases;')
records = cursor.fetchall()
for r in records:
    print(r)

cursor.close()
connection.close()
