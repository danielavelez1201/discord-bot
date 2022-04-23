
import mysql.connector

cnx = mysql.connector.connect(host="localhost",
        user="danielavelez1201@gmail.com",
        password="Lailabeth2000*", port="3306", 
        database="athena")

cursor = cnx.cursor()
try:
    table_to_delete = input("Which table do you want to delete? ")
    cursor.execute("DROP TABLE " + table_to_delete)
except mysql.connector.Error as err:
  print("Something went wrong: {}".format(err))
