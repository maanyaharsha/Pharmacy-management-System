import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    username="root",
    password="Maanya@2005",
    database="pharmacy"
)

print("Database Connected Successfully")