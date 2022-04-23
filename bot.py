import mysql.connector
import discord 
from discord.ext import commands



print(discord.__version__)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='', intents=intents)

cnx = mysql.connector.connect(host="localhost",
    user="danielavelez1201@gmail.com",
    password="Lailabeth2000*", port="3306", 
    database="athena")
cursor = cnx.cursor()

@bot.command()
async def Hi(ctx):
 await ctx.send("Hi, welcome to our server")


"""
<Message id=967098726432800798 
channel=<TextChannel 
id=966704306822742029 
name='general' 
position=0 
nsfw=False 
news=False 
category_id=966704306822742027> 
type=<MessageType.default: 0> 
author=<Member id=909705923038154763 
name='Daniela Velez' 
discriminator='9977' 
bot=False nick=None 
guild=<Guild id=966704306235519118 
name='trial server' 
shard_id=None 
chunked=False 
member_count=2>> 
flags=<MessageFlags value=0>>

<Message id=967104511925715025 
channel=<Thread id=967098726432800798 
name='trial' parent=general 
owner_id=909705923038154763 
locked=False archived=False> 
type=<MessageType.default: 0> 
author=<Member id=909705923038154763 
name='Daniela Velez' 
discriminator='9977' 
bot=False nick=None 
guild=<Guild id=966704306235519118 
name='trial server' 
shard_id=0 chunked=True member_count=2>> 
flags=<MessageFlags value=0>>
"""

@bot.command()
async def summary(ctx):
    request_sql = "SELECT * FROM messages"
    cursor.execute(request_sql)
    result = cursor.fetchall()
    await ctx.send(result)

@bot.event
async def on_message(msg):
    id = msg.id
    author = msg.author
    server = msg.author.guild
    text = msg.content
    print(f"{server.id}, {server.name}, {server.member_count}")
    print(f"{author.id}, {author.name}, {author.nick}, {server.id}")
    print(f"{id}, {author.id}, {server.id}, {text}")

    server_sql = "INSERT IGNORE INTO servers (id, name, member_count) VALUES (%s, %s, %s)"
    server_vals = [server.id, server.name, server.member_count]
    try:
        cursor.execute(server_sql, server_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into servers.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    
    user_sql = "INSERT IGNORE INTO users (id, name, nick, server_id) VALUES (%s, %s, %s, %s)"
    user_vals = [author.id, author.name, author.nick, server.id]
    try:
        cursor.execute(user_sql, user_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into users.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    message_sql = "INSERT INTO messages (id, author_id, server_id, text) VALUES (%s, %s, %s, %s)"
    message_vals = [id, author.id, server.id, text]
    try:
        cursor.execute(message_sql, message_vals)
        cnx.commit()
        print(cursor.rowcount, "record inserted into messages.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    
    if 'word' in msg.content:
        print('hi')
       

Secret = open("secret.txt", 'r')
Secret = Secret.read()
bot.run(Secret)