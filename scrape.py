import requests
import json

def retrieve_messages(channelid):
    num = 0
    limit = 100

    headers = {
        'authorization': 'INSERT_AUTHORIZATION HEADER(FROM DEV CONSOLE)'
    }

    last_message_id = None
    retString = "message_id, message_content, user_id, timestamp\n"

    while True:
        query_parameters = f'limit={limit}'
        if last_message_id is not None:
            query_parameters += f'&before={last_message_id}'

        r = requests.get(
            f'https://discord.com/api/v9/channels/{channelid}/messages?{query_parameters}',headers=headers
            )
        jsonn = json.loads(r.text)
            

        for value in jsonn:
            retString += value['id'] + "," + value['content'] + "," + value['author']['id'] + "," + value['timestamp'] + ";;;; \n"
            #print(value['content'], '\n')
            last_message_id = value['id']
            num=num+1
        if num == 25251:
            print('number of messages we collected is',num)
            print(retString)
            with open('near-messages.txt', 'w') as f:
                f.write(retString)
            break
        print(num)
    # print('number of messages we collected is',num)
    # print(retString)
    # with open('near-messages.txt', 'w') as f:
    #     f.write(retString)

retrieve_messages('542945453533036544')


#Format: 
#message_id, message_content, user_id, timestamp
#Start printing it out like this 
#write to a file 
