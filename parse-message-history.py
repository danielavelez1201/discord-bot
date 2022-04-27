from gpt3 import extract_keywords
from db_update import addKeywordsToDB, addMessage, addQuestionIDtoKeywords, addUser, addServer

f = open("near-messages.txt", "r")

text = f.read()

text = text.split(";;;;")

text = text[1:]
text = text[:-1]

#message_id, message_content, user_id, timestamp

def parse_and_get_keywords():
    addServer(490367152054992913, "", -1)
    counter = 0
    for line in text: 
        if counter == 10:
            return
        lineArr = line.split(",")
        messageId = lineArr[0]
        timestamp = lineArr[-1]
        userId = lineArr[-2]
        content = lineArr[1:-2]
        content = "".join(content)
        keywords = extract_keywords(content)
        addUser(int(userId), "", "", 490367152054992913)
        addKeywordsToDB(keywords)
        addMessage(int(messageId), int(userId), 490367152054992913, content, 0)
        addQuestionIDtoKeywords(int(messageId), keywords)
        counter += 1

parse_and_get_keywords()