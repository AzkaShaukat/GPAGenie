import mysql.connector

db = (mysql.connector.connect
    (
    host="localhost",
    user="root",
    password=""
))

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
print("MySQL version:", cursor.fetchone()[0])