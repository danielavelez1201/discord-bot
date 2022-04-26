f = open("near-messages.txt", "r")

text = f.read()

text = text.split(";;;;")
print(len(text))

text = text[1:]
text = text[:-1]

jsonData = []

#message_id, message_content, user_id, timestamp

for line in text: 
    lineArr = line.split(",")
    messageId = lineArr[0]
    timestamp = lineArr[-1]
    userId = lineArr[-2]
    content = lineArr[1:-2]
    content = "".join(content)
    jsonData.append({
        "content": content, 
        "userId": userId, 
        "timestamp": timestamp, 
        "messageId" : messageId
    })

print(len(jsonData))
