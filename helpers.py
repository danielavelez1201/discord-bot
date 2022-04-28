from db_fetch import *

def db_result_to_string(l):
    result = ""
    for row in l:
        for item in row:
            result += str(item)
    return result

def format_author_name(name, nick):
    return name + (' (' + nick + ')' if nick else '')

def format_answer_string(answer):
    if not answer:
        return ''
    result = f"""
        \n
        {answer['author']}: {answer['body']}\n
        {answer['link']}\n
        Upvotes: {answer['upvotes']}\n
        Accepted: {answer['accepted']}
    """
    return result

def format_question_string(question):
    result = f"""{question['title'] if question['title'] != '' else ''}
        {question['author'] + ':' if question['author'] != '' else ''} {question['body']}
        {question['link']}
        Upvotes: {question['upvotes']}\n
        {format_answer_string(question['answer'])}"""
    return result

def similar_questions_formatted(questions):
    result_string = ""
    for id, author_id, title, body, upvotes, answered in questions:
        server_id = 490367152054992913
        question_dict = {}
        question_dict['link'] = create_link(server_id, author_id, id)

        name, nick = get_user_with_id(author_id)
        question_dict['author'] = format_author_name(name, nick)
        question_dict['title'] = title
        question_dict['body'] = body
        question_dict['upvotes'] = upvotes
        question_dict['answer'] = None

        if answered:
            answer_id, answer_author_id, answer_body, answer_upvotes, answer_accepted = get_answer_with_question_id(id)
            answer_author_name, answer_author_nick = get_user_with_id(answer_author_id)
            answer_link = create_link(server_id, answer_author_id, answer_id)
            question_dict['answer'] = {
                'link': answer_link,
                'author': format_author_name(answer_author_name, answer_author_nick),
                'body': answer_body,
                'upvotes': answer_upvotes,
                'accepted': answer_accepted,
                }
        result_string += format_question_string(question_dict)
    return result_string   

def askQuestionSuggestions(keywords):
    message_intro = "You might want to check these out:"
    questions = get_similar_questions(keywords)
    return message_intro + similar_questions_formatted(questions)