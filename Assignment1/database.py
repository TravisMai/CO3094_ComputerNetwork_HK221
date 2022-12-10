import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    port = 3307
)
mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE pythonDatabase")
mycursor.execute("CREATE TABLE login_info (username VARCHAR(45), password VARCHAR(45))")

sql = "INSERT INTO login_info (username, password) VALUES (%s, %s)"
