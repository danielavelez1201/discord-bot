import csv 
import requests
import json

def get_server_ids():
    result = []
    with open('../../general_data/server_ids.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            if row[0] == '':
                return result
            if row[6] != '' and row[6] != "#N/A":
                result.append({
                    'name': row[0],
                    'id': row[6]
                })
    return result
     
def retrieve_messages(server_info):
    channel_id = server_info['id']
    channel_name = server_info['name']
    print(channel_name, channel_id)

    num = 0
    limit = 100

    headers = {
        'authorization': 'Bot 5bd249ab4edfc09ecbaf9e491de6db22c0b5b122039d440ebafde9567af8292b'
    }

    last_message_id = None
    retString = "message_id, message_content, user_id, timestamp\n"

    query_parameters = f'limit={limit}'
    if last_message_id is not None:
        query_parameters += f'&before={last_message_id}'

    r = requests.get(
        f'https://discord.com/api/v9/channels/{channel_id}/messages?{query_parameters}',headers=headers
        )
    jsonn = json.loads(r.text)
    print(jsonn)
    for value in jsonn:
        retString += value['id'] + "," + value['content'] + "," + value['author']['id'] + "," + value['timestamp'] + ";;;; \n"
        #print(value['content'], '\n')
        last_message_id = value['id']
        num=num+1
    print('number of messages we collected is',num)
    print(retString)
    with open(f'{channel_name}-messages.txt', 'w') as f:
        f.write(retString)


def scrape_discord_servers():
    servers = get_server_ids()
    for server in servers:
        try:
            retrieve_messages(server)
        except Exception as err:
            print("skipped this server: ", err)
        
scrape_discord_servers()