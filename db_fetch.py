from config import cursor, BOT_NAME


def allMessages():
    request_sql = "SELECT * FROM messages"
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result


def get_user_id_from_answer_id(answer_id):
    request_sql = "SELECT author_id FROM answers WHERE id = " + str(answer_id)
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result


def get_question_from_answer_id(answer_id):
    result = get_question_id_from_answer_id(answer_id)
    if len(result) > 0:
        q_id = result[0][0]
        request_sql = "SELECT author_id FROM questions WHERE id = " + str(q_id)
        cursor.execute(request_sql)
        result = cursor.fetchall()
        return result
    return []


def get_question_id_from_answer_id(answer_id):
    request_sql = "SELECT question_id FROM answers WHERE id = " + str(answer_id)
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


def get_answer_question_from_answer_id(answer_id):
    request_sql = "SELECT author_id, question_id FROM answers WHERE id = " + str(
        answer_id
    )
    cursor.execute(request_sql)
    result = cursor.fetchone()
    if result:
        (answer_author_id, question_id) = result
        request_sql = "SELECT author_id FROM questions WHERE id = " + str(question_id)
        cursor.execute(request_sql)
        result = cursor.fetchone()
        if result:
            (question_author_id,) = result
            return (
                {"id": answer_id, "author_id": answer_author_id},
                {"id": question_id, "author_id": question_author_id},
            )
    return (None, None)


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
