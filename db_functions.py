import mysql.connector

BOT_NAME = 'athena'

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

def fetchMessagesFormatted():
    request_sql = """
        SELECT * FROM messages 
        ORDER BY created_at
    """
    cursor.execute(request_sql)
    messages = cursor.fetchall()
    result = ""
    for (id, author_id, server_id, text, created_at, updated_at) in messages:
        author_sql = f"""
            SELECT name 
            FROM users 
            WHERE id = {author_id}"""
        cursor.execute(author_sql)
        author_name = cursor.fetchall()[0][0]
        print(author_name)
        if author_name != BOT_NAME:
            result += author_name + ": "
            result += text + "\n"
    return result
