def format_author_name(name, nick):
    return name + (' (' + nick + ')' if nick else '')

def format_answer_string(answer, include_upvotes=False, include_accepted=False):
    if not answer:
        return ''

    upvotes_str = f"Upvotes: {answer['upvotes']}\n"
    accepted_str = f"Accepted: {answer['accepted']}"

    result = f"""
    \n
    {answer['author']}: {answer['body']}\n
    {answer['link']}\n
    {upvotes_str if include_upvotes else ''}
    {accepted_str if include_accepted else ''}
    """
    return result

def format_question_string(question, include_upvotes=False):
    upvotes_str = f"Upvotes: {question['upvotes']}\n"

    result = f"""**{question['title'] if question['title'] != '' else ''}**
    {question['author'] + ':' if question['author'] != '' else ''} {question['body']}
    [Go to question]({question['link']})
    {upvotes_str if include_upvotes else ''}
    {format_answer_string(question['answer'])}"""
    return result
