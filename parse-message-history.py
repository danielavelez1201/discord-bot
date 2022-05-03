from utils.gpt3 import extract_keywords
from db.functions.db_update import (
    addKeywordsToDB,
    addMessage,
    addMessageIDToKeywords,
    addUser,
    addServer,
)

from db.functions.db_fetch import getMessages

f = open("near-messages.txt", "r")

text = f.read()

text = text.split(";;;;")

text = text[1:]
text = text[:-1]

# message_id, message_content, user_id, timestamp


def parse_and_get_keywords():
    addServer(490367152054992913, "", -1)
    counter = 0
    for line in text:
        lineArr = line.split(",")
        messageId = lineArr[0].strip()
        timestamp = lineArr[-1]
        userId = lineArr[-2]
        content = lineArr[1:-2]
        content = "".join(content)
        addUser(int(userId), "", "", 490367152054992913)
        addMessage(int(messageId), int(userId), 490367152054992913, content, 0)
        counter += 1


def get_keywords():
    count = 5
    messages = getMessages()[5:]
    for (
        message_id,
        author_id,
        server_id,
        text,
        upvotes,
        created_at,
        updated_at,
    ) in messages:
        keywords = extract_keywords(text)
        addKeywordsToDB(keywords)
        addMessageIDToKeywords(int(message_id), keywords)
        count += 1
        print(count)
    return


get_keywords()
