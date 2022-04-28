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
