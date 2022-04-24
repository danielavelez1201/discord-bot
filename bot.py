import mysql.connector
import discord 
from discord.ext import commands
import db_functions
import helpers

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='', intents=intents)

cnx = mysql.connector.connect(host="localhost",
    user="danielavelez1201@gmail.com",
    password="Lailabeth2000*", port="3306", 
    database="athena")
cursor = cnx.cursor()

@bot.command()
async def summary(ctx):
    result = db_functions.fetchMessagesFormatted()
    await ctx.send(result)

@bot.listen()
async def on_message(msg):
    if msg.author.bot:
        return
    id = msg.id
    author = msg.author
    server = msg.author.guild
    text = msg.content

    if "#q" in text:
        message = "You might want to check these out: \n"
        db_result = db_functions.fetchMessagesFormatted()
        response = message + db_result
        await msg.channel.send(response)

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
    
    bot.process_commands(msg)
       

Secret = open("secret.txt", 'r')
Secret = Secret.read()
bot.run(Secret)