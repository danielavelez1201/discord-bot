import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    user="athena-admin",
    password="abc123",
    port="3306",
    database="athena",
)

cursor = cnx.cursor()
table_to_delete = input("Which table do you want to delete? ")
if (table_to_delete == "all"):
    for table_name in ['users_servers', 'users', 'servers', 'messages', 'keywords_questions', 'keywords', 'questions', 'answers', 'keywords_answers']:
        try:
            cursor.execute("DROP TABLE " + table_name)
            print('deleted ', table_name)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
else:    
    try: 
        cursor.execute("DROP TABLE " + table_to_delete)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
