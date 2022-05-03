from config import cursor, BOT_NAME


"""
Retrieving user id and info.
"""

# From answer
def get_user_id_from_answer_id(answer_id):
    request_sql = "SELECT author_id FROM answers WHERE id = " + str(answer_id)
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result[0]


# From question corresponding answer
def get_user_id_from_question_id_for_answer(answer_id):
    result = get_question_id_from_answer_id(answer_id)
    if len(result) > 0:
        q_id = result[0][0]
        request_sql = "SELECT author_id FROM questions WHERE id = " + str(q_id)
        cursor.execute(request_sql)
        result = cursor.fetchall()
        return result[0]
    return None


# From message
def get_user_id_from_message_id(message_id):
    request_sql = "SELECT author_id FROM messages WHERE id = " + str(message_id)
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result[0]


# Name, nickname from id
def get_user_with_id(id):
    user_sql = f"SELECT name, nick FROM users WHERE id = {id}"
    cursor.execute(user_sql)
    return cursor.fetchall()[0]


"""
Retrieving question, message, and answer id and info.
"""

# Id from answer
def get_question_id_from_answer_id(answer_id):
    request_sql = f"SELECT question_id FROM answers WHERE id = '{str(answer_id)}'"
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result[0]


# Question tuple from id
def get_question_with_id(id):
    question_sql = f"SELECT id, author_id, title, body, upvotes, answered FROM questions WHERE id = {id}"
    cursor.execute(question_sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return None
    return result[0]

<<<<<<< HEAD
# Message tuple from id, in question tuple format optionally
def get_message_with_id_with_question_format(id, question_format=True):
=======

# Message tuple from id, in question tuple format
def get_message_with_id_with_question_format(id):
>>>>>>> 2240ce2d64a0203cff9cbf2f776e9bc13f304c5b
    message_sql = f"SELECT id, author_id, text, upvotes FROM messages WHERE id = {id}"
    cursor.execute(message_sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return None
    if question_format:
        id, author_id, text, upvotes = result[0]
        return (id, author_id, "", text, upvotes, False)
    else:
        return result[0]


# Question/message tuple from id
def get_question_or_message_with_id(id):
    question_query = get_question_with_id(id)
    message_query = get_message_with_id_with_question_format(id)
    return question_query if question_query else message_query


# Answer corresponding to question id
def get_answer_with_question_id(id):
    answer_sql = f"SELECT id, author_id, body, upvotes, accepted FROM answers WHERE question_id = {id}"
    cursor.execute(answer_sql)
    return cursor.fetchall()[0]


"""
Retrieving relevant questions, messages, and answers.
"""

# Questions
def get_question_ids_with_keyword(keyword):
    question_sql = (
        f'SELECT question_id FROM keywords_questions WHERE word = "{keyword}"'
    )
    cursor.execute(question_sql)
    question_ids = cursor.fetchall()
    return question_ids


# Messages
def get_message_ids_with_keyword(keyword):
    message_sql = f'SELECT message_id FROM keywords_messages WHERE word = "{keyword}"'
    cursor.execute(message_sql)
    message_ids = cursor.fetchall()
    return message_ids


# Answers
def get_answer_ids_with_keyword(keyword):
    answer_sql = f'SELECT answer_id FROM keywords_answers WHERE word = "{keyword}"'
    cursor.execute(answer_sql)
    answer_ids = cursor.fetchall()
    return answer_ids


# Questions based on answers
def get_question_ids_with_relevant_answers(keyword):
    answer_ids = get_answer_ids_with_keyword(keyword)
    return [get_question_id_from_answer_id(id[0]) for id in answer_ids]


"""
Retrieving contributor info.
"""

# Author score
def get_score_from_author(user_id):
    request_sql = "SELECT contribution_score FROM users WHERE id = " + str(user_id)
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result


# Top contributors
def get_top_contributors(count):
    request_sql = "SELECT * FROM users ORDER BY contribution_score ASC LIMIT " + str(
        count
    )
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result


"""
Retrieving all messages.
"""


def all_messages():
    request_sql = "SELECT * FROM messages"
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result


def messagesFormatted():
    request_sql = """
        SELECT * FROM messages 
        ORDER BY created_at
    """
    cursor.execute(request_sql)
    messages = cursor.fetchall()
    result = ""
    for (id, author_id, server_id, text, upvotes, created_at, updated_at) in messages:
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


def getMessages():
    request_sql = """
        SELECT * FROM messages ORDER BY created_at DESC;
    """
    cursor.execute(request_sql)
    messages = cursor.fetchall()
    return messages
