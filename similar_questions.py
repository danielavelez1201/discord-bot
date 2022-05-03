from db.functions.db_fetch import *
from utils.helpers import *
from utils.formatting import *

def get_similar_questions(keywords):
    """
    Input: List of keywords (e.g. ['blockchain', 'admin'])
    Output: List of relevant question/message tuples (id, author_id, title, body, upvotes, answered)
    """
    freqs = {}
    for word in keywords:
        all_matching = get_question_ids_with_keyword(word) + get_message_ids_with_keyword(word) + get_question_ids_with_relevant_answers(word)
        for id in all_matching:
            freqs[id[0]] = freqs.get(id[0], 0) + 1

    result_list = list(freqs.items())
    result_list.sort(key=lambda x: x[1])
    if len(result_list) > 5:
        result_list = result_list[0:6]

    return [get_question_or_message_with_id(id_tup[0]) for id_tup in result_list]


def similar_questions_formatted(questions):
    """
    Input: List of question/message tuples (id, author_id, title, body, upvotes, answered)
    Output: Formatted string of questions
    """
    result_string = ""
    for id, message_id, author_id, title, body, upvotes, answered in questions:
        server_id = 490367152054992913
        question_dict = {}
        question_dict['link'] = create_link(server_id, author_id, message_id)

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


def ask_question_suggestions(keywords, gpt3_on=True):
    """
    Input: List of keywords (e.g. ['blockchain', 'admin'])
    Output: String to send in channel with relevant questions
    """
    message_intro = "You might want to check these out:\n\n"
    
    if not gpt3_on:
        return message_intro + "similar questions!"

    questions = get_similar_questions(keywords)
    return message_intro + similar_questions_formatted(questions)
