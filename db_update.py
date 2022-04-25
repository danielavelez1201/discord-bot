from wsgiref.util import request_uri
import mysql.connector

cnx = mysql.connector.connect(host="localhost",
    user="danielavelez1201@gmail.com",
    password="Lailabeth2000*", port="3306", 
    database="athena")
cursor = cnx.cursor()

def addServerToDB(server_id, server_name, server_member_count):
    server_sql = "INSERT IGNORE INTO servers (id, name, member_count) VALUES (%s, %s, %s)"
    server_vals = [server_id, server_name, server_member_count]
    try:
        cursor.execute(server_sql, server_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into servers.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addContributionToDB(new_contribution_score, user_id):
    contribution_sql = "UPDATE users SET contribution_score = " + str(new_contribution_score) + " WHERE id = " + str(user_id)
    try:
        cursor.execute(contribution_sql)
        cnx.commit()
        print(cursor.rowcount, "record inserted into users.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addAuthorToDB(author_id, author_name, author_nick, server_id):
    user_sql = "INSERT IGNORE INTO users (id, name, nick, server_id) VALUES (%s, %s, %s, %s)"
    user_vals = [author_id, author_name, author_nick, server_id]
    try:
        cursor.execute(user_sql, user_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into users.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def addMessageToDB(id, author_id, server_id, text):
    message_sql = "INSERT INTO messages (id, author_id, server_id, text) VALUES (%s, %s, %s, %s)"
    message_vals = [id, author_id, server_id, text]
    try:
        cursor.execute(message_sql, message_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into messages.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def addKeywordToDB(word):
    keyword_sql = "INSERT INTO keywords (word, question_ids) VALUES (%s, %s)"
    keyword_vals = [word, []]
    try:
        cursor.execute(keyword_sql, keyword_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into keywords.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addQuestionIDtoKeywords(question_id, keywords):
    try:
        for word in keywords:
            request_sql = f"SELECT question_ids FROM keywords WHERE word == {word}"
            cursor.execute(request_sql)
            result = cursor.fetchall()
            updated_question_array = result.append(question_id)
            sql = f"UPDATE keywords SET question_ids = {updated_question_array}"
            cursor.execute(sql)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    
