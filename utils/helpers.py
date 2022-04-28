import sys

def db_result_to_string(l):
    result = ""
    for row in l:
        for item in row:
            result += str(item)
    return result

def create_link(server_id, author_id, message_id):
    return (
        "https://discord.com/channels/"
        + str(server_id)
        + "/"
        + str(author_id)
        + "/"
        + str(message_id)
    )
