import mysql.connector
import discord 
from discord.ext import commands
import db_fetch
import helpers
import db_update

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='', intents=intents)

cnx = mysql.connector.connect(host="localhost",
    user="danielavelez1201@gmail.com",
    password="Lailabeth2000*", port="3306", 
    database="athena")
cursor = cnx.cursor()

async def handleQuestion(msg):
    message = "You might want to check these out: \n"
    db_result = db_fetch.messagesFormatted()
    response = message + db_result
    await msg.channel.send(response)

@bot.command()
async def summary(ctx):
    result = db_fetch.messagesFormatted()
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
        handleQuestion(msg)

    db_update.addServerToDB(server.id, server.name, server.member_count)
    db_update.addAuthorToDB(author.id, author.name, author.nick, server.id)
    db_update.addMessageToDB(id, author.id, server.id, text)
    
    bot.process_commands(msg)
       

Secret = open("secret.txt", 'r')
Secret = Secret.read()
bot.run(Secret)