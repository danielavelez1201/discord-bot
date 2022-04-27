import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    user="athena-admin",
    password="abc123",
    port="3306",
    database="athena",
)

cursor = cnx.cursor()

cursor.execute("SHOW FULL COLUMNS FROM keywords")
result = cursor.fetchall()
print(result)

cursor.execute("SELECT * FROM keywords")
result = cursor.fetchall()
print(result)
