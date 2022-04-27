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


def get_top_contributors(count):
    request_sql = "SELECT * FROM users ORDER BY contribution_score ASC LIMIT " + str(
        count
    )
    cursor.execute(request_sql)
    result = cursor.fetchall()
    return result


def get_similar_question_ids(keywords):
    all_question_ids = set()
    for word in keywords:
        question_sql = (
            f"SELECT question_id FROM keywords_questions WHERE word = '{word}'"
        )
        cursor.execute(question_sql)
        question_result = cursor.fetchall()
        message_sql = f"SELECT message_id FROM keywords_messages WHERE word = '{word}'"
        cursor.execute(message_sql)
        message_result = cursor.fetchall()
        if len(question_result) > 0:
            all_question_ids = all_question_ids.union(question_result[0])
        if len(message_result) > 0:
            all_question_ids = all_question_ids.union(message_result[0])
    return list(all_question_ids)


def create_link(server_id, author_id, message_id):
    return (
        "https://discord.com/channels/"
        + str(server_id)
        + "/"
        + str(author_id)
        + "/"
        + str(message_id)
    )


def get_question_with_id(id):
    question_sql = f"SELECT id, author_id, title, body, upvotes, answered FROM questions WHERE id = {id}"
    cursor.execute(question_sql)
    return cursor.fetchall()[0]


def get_answer_with_question_id(id):
    answer_sql = f"SELECT id, author_id, body, upvotes, accepted FROM answers WHERE question_id = {id}"
    cursor.execute(answer_sql)
    return cursor.fetchall()[0]


def get_author_with_id(id):
    author_sql = f"SELECT name, nick FROM users WHERE id = {id}"
    cursor.execute(author_sql)
    return cursor.fetchall()[0]


def format_author_name(name, nick):
    return name + (" (" + nick + ")" if nick != "" else "")


def similar_questions_formatted(question_ids):
    result_dicts = []
    for question_id in question_ids:
        question = get_question_with_id(question_id)
        server_id = 490367152054992913
        question_format = {}
        for id, author_id, title, body, upvotes, answered in question:
            question_format["link"] = create_link(server_id, author_id, id)

            name, nick = get_author_with_id(author_id)
            question_format["author_name"] = format_author_name(name, nick)
            question_format["title"] = title
            question_format["body"] = body
            question_format["upvotes"] = upvotes

            if answered:
                (
                    answer_id,
                    answer_author_id,
                    answer_body,
                    answer_upvotes,
                    answer_accepted,
                ) = get_answer_with_question_id(id)
                answer_author_name, answer_author_nick = get_author_with_id(
                    answer_author_id
                )
                answer_link = create_link(server_id, answer_author_id, answer_id)
                question_format["answer"] = {
                    "link": answer_link,
                    "author": format_author_name(
                        answer_author_name, answer_author_nick
                    ),
                    "body": answer_body,
                    "upvotes": answer_upvotes,
                    "accepted": answer_accepted,
                }
        result_dicts.append(question_format)
    return result_dicts


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
