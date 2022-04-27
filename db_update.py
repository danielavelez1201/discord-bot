from mysql.connector import Error
from config import cursor, cnx


def addServer(server_id, name, member_count):
    server_sql = (
        "INSERT IGNORE INTO servers (id, name, member_count) VALUES (%s, %s, %s)"
    )
    server_vals = [server_id, name, member_count]
    try:
        cursor.execute(server_sql, server_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into servers.")
    except Error as err:
        print("Something went wrong: {}".format(err))


def addUser(author_id, author_name, author_nick, server_id):
    user_sql = "INSERT IGNORE INTO users (id, name, nick) VALUES (%s, %s, %s)"
    user_vals = [author_id, author_name, author_nick]
    user_server_junction_sql = (
        "INSERT IGNORE INTO users_servers (user_id, server_id) VALUES (%s, %s)"
    )
    junction_vals = [author_id, server_id]
    try:
        cursor.execute(user_sql, user_vals)
        cursor.execute(user_server_junction_sql, junction_vals)
        cnx.commit()
        print(
            cursor.rowcount,
            "record inserted into users and user server junction table.",
        )
    except Error as err:
        print("Something went wrong: {}".format(err))


def addKeyword(word):
    keyword_sql = "INSERT IGNORE INTO keywords (word) VALUES (%s)"
    keyword_vals = [word]
    try:
        cursor.execute(keyword_sql, keyword_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into keywords.")
    except Error as err:
        print("Something went wrong: {}".format(err))


def addQuestion(author_id, server_id, title, body, bounty, upvotes, answered, keyword):
    question_sql = "INSERT IGNORE INTO questions (author_id, server_id, title, body, bounty, upvotes, answered) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    question_vals = [
        author_id,
        server_id,
        title,
        body,
        bounty,
        upvotes,
        answered,
    ]
    try:
        cursor.execute(question_sql, question_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into questions.")
        question_id = cursor.lastrowid
        question_junction_sql = (
            "INSERT IGNORE INTO keywords_questions (question_id, word) VALUES (%s, %s)"
        )
        question_junction_vals = [question_id, keyword]
        cursor.execute(question_junction_sql, question_junction_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into question keyword junction table.")
        return question_id
    except Error as err:
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
    except Error as err:
        print("Something went wrong: {}".format(err))


def addMessage(id, author_id, server_id, text, upvotes, keyword=None):
    message_sql = "INSERT IGNORE INTO messages (id, author_id, server_id, text, upvotes) VALUES (%s, %s, %s, %s, %s)"
    message_vals = [id, author_id, server_id, text, upvotes]
    if keyword:
        message_junction_sql = (
            "INSERT IGNORE INTO keywords_messages (message_id, word) VALUES (%s, %s)"
        )
        message_junction_vals = [id, keyword]
    try:
        cursor.execute(message_sql, message_vals)
        if keyword:
            cursor.execute(message_junction_sql, message_junction_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into messages and messages junction.")
    except Error as err:
        print("Something went wrong: {}".format(err))


def addAnswer(id, author_id, question_id, server_id, body, upvotes, accepted, keyword):
    answer_sql = "INSERT IGNORE INTO answers (id, author_id, question_id, server_id, body, upvotes, accepted) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    answer_vals = [
        id,
        author_id,
        question_id,
        server_id,
        body,
        upvotes,
        accepted,
    ]
    answer_junction_sql = (
        "INSERT IGNORE INTO keywords_answers (answer_id, word) VALUES (%s, %s)"
    )
    answer_junction_vals = [id, keyword]
    try:
        cursor.execute(answer_sql, answer_vals)
        cursor.execute(answer_junction_sql, answer_junction_vals)
        cnx.commit()
        print(
            cursor.rowcount,
            "record inserted into answers and answer keywords junction.",
        )
    except Error as err:
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
    except Error as err:
        print("Something went wrong: {}".format(err))


def addKeywordsToDB(words):
    for word in words:
        addKeyword(word)


def addQuestionIDtoKeywords(question_id, keywords):
    try:
        for word in keywords:
            addKeyword(word)
            question_keyword_junction_sql = "INSERT IGNORE INTO keywords_questions (question_id, word) VALUES (%s, %s)"
            cursor.execute(question_keyword_junction_sql, [question_id, word])
            cnx.commit()
            print(cursor.rowcount, "record inserted for keyword and question.")
    except Error as err:
        print("Something went wrong: {}".format(err))
