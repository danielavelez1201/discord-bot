import mysql.connector

BOT_NAME = 'athena'

cnx = mysql.connector.connect(host="localhost",
    user="danielavelez1201@gmail.com",
    password="Lailabeth2000*", port="3306", 
    database="athena")
cursor = cnx.cursor()

def allMessages():
    request_sql = "SELECT * FROM messages"
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result

def get_author_from_message(message_id):
    request_sql = "SELECT author_id FROM messages WHERE id = " + str(message_id)
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result

def get_score_from_author(user_id):
    request_sql = "SELECT contribution_score FROM users WHERE id = " + str(user_id)
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result

def get_similar_question_ids(keywords):
    all_question_ids = set()
    for word in keywords:
        request_sql = f"SELECT question_ids FROM keywords WHERE word = {word}"
        cursor.execute(request_sql)
        result = cursor.fetchall()
        all_question_ids = all_question_ids.union(result[0])
    return list(all_question_ids)

def messagesFormatted():
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
        if author_name != BOT_NAME:
            result += author_name + ": "
            result += text + "\n"
    return result


