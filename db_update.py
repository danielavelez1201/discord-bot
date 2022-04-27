import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    user="athena-admin",
    password="abc123",
    port="3306",
    database="athena",
)
cursor = cnx.cursor()


def addServer(server_id, name, member_count):
    server_sql = (
        "INSERT IGNORE INTO servers (id, name, member_count) VALUES (%s, %s, %s)"
    )
    server_vals = [server_id, name, member_count]
    try:
        cursor.execute(server_sql, server_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into servers.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addUser(author_id, author_name, author_nick, server_id):
    user_sql = (
        "INSERT IGNORE INTO users (id, name, nick, server_id) VALUES (%s, %s, %s, %s)"
    )
    user_vals = [author_id, author_name, author_nick, server_id]
    try:
        cursor.execute(user_sql, user_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into users.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addKeyword(word, server_id):
    keyword_sql = "INSERT IGNORE INTO keywords (word, server_id) VALUES (%s, %s)"
    keyword_vals = [word, server_id]
    try:
        cursor.execute(keyword_sql, keyword_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into keywords.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addQuestion(author_id, server_id, title, body, bounty, upvotes, answered, keyword):
    question_sql = "INSERT INTO questions (author_id, server_id, title, body, bounty, upvotes, answered, keyword) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    question_vals = [
        author_id,
        server_id,
        title,
        body,
        bounty,
        upvotes,
        answered,
        keyword,
    ]
    try:
        cursor.execute(question_sql, question_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into questions.")
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addContribution(new_contribution_score, user_id):
    contribution_sql = (
        "UPDATE users SET contribution_score = "
        + str(new_contribution_score)
        + " WHERE id = "
        + str(user_id)
    )
    try:
        cursor.execute(contribution_sql)
        cnx.commit()
        print(cursor.rowcount, "record inserted into users.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addMessage(id, author_id, server_id, text, upvotes):
    message_sql = "INSERT INTO messages (id, author_id, server_id, text, upvotes) VALUES (%s, %s, %s, %s, %s)"
    message_vals = [id, author_id, server_id, text, upvotes]
    try:
        cursor.execute(message_sql, message_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into messages.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def addAnswer(id, author_id, question_id, server_id, body, upvotes, accepted, keyword):
    answer_sql = "INSERT INTO answers (id, author_id, question_id, server_id, body, upvotes, accepted, keyword) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    answer_vals = [
        id,
        author_id,
        question_id,
        server_id,
        body,
        upvotes,
        accepted,
        keyword,
    ]
    try:
        cursor.execute(answer_sql, answer_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into answers.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def acceptAnswer(questionId, answerId):
    accept_q_sql = "UPDATE questions SET answered = 1 WHERE id = " + str(questionId)
    accept_a_sql = "UPDATE answers SET accepted = 1 WHERE id = " + str(answerId)
    try:
        cursor.execute(accept_q_sql)
        cnx.commit()
        cursor.execute(accept_a_sql)
        cnx.commit()
        print(cursor.rowcount, "record updated for accepted answer and question.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
