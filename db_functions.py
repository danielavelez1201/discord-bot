import mysql.connector

cnx = mysql.connector.connect(host="localhost",
    user="danielavelez1201@gmail.com",
    password="Lailabeth2000*", port="3306", 
    database="athena")
cursor = cnx.cursor()

def fetchAllMessages():
    request_sql = "SELECT * FROM messages"
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result

def fetchMostRecentMessages():
    request_sql = "SELECT text FROM messages"
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result
