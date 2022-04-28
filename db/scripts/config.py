from mysql.connector import connect

cnx = connect(
    host="localhost",
    user="athena-admin",
    password="abc123",
    port="3306",
    database="athena",
)

delimiter = "&$,|"

cursor = cnx.cursor()
