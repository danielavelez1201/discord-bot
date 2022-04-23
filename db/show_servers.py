import mysql.connector

cnx = mysql.connector.connect(host="localhost",
        user="danielavelez1201@gmail.com",
        password="Lailabeth2000*", port="3306", 
        database="athena")

cursor = cnx.cursor()

cursor.execute("SHOW FULL COLUMNS FROM servers")
result = cursor.fetchall()
print(result)

cursor.execute("SELECT * FROM servers")
result = cursor.fetchall()
print(result)