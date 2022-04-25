import mysql.connector
import discord 
from discord.ext import commands
import db_fetch
import helpers
import db_update
import os
import gpt3

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='', intents=intents)

cnx = mysql.connector.connect(host="localhost",
    user="danielavelez1201@gmail.com",
    password="Lailabeth2000*", port="3306", 
    database="athena")
cursor = cnx.cursor()

async def handleQuestion(msg):
    print("PRINTING HANDLE QUESTION NOW")
    message_intro = "You might want to check these out: \n"
    db_result = db_fetch.messagesFormatted()
    message_tag = str(msg.id)[-4:]
    message_end = f"\n To respond to this question, add #{message_tag}"
    response = message_intro + db_result + message_end
    await msg.channel.send(response)

@bot.command()
async def summary(ctx):
    print("printing summary now")
    result = db_fetch.messagesFormatted()
    await ctx.send(result)

@bot.listen()
async def on_reaction_add(reaction, user):
    print(reaction.message.id)
    user_id = db_fetch.get_author_from_message(reaction.message.id)[0][0]
    current_contribution_score = db_fetch.get_score_from_author(user_id)[0][0]
    #Need to check if this is a real answer 
    db_update.addContributionToDB(current_contribution_score + 1, user_id)
    

#Store reacts of answers
#To calculate contributor ranking -> look at reacts people with the most answers and positive reacts 
@bot.listen()
async def on_message(msg):
    print("PRINTING ON MESSAGE NOW")
    print(msg.id)
    if msg.author.bot:
        return
    id = msg.id
    author = msg.author
    server = msg.author.guild
    text = msg.content

    if "#q" in text:
        await handleQuestion(msg)

    db_update.addServerToDB(server.id, server.name, server.member_count)
    db_update.addAuthorToDB(author.id, author.name, author.nick, server.id)
    db_update.addMessageToDB(id, author.id, server.id, text)
    
    await bot.process_commands(msg)
       

Secret = open("secret.txt", 'r')
Secret = Secret.read()
bot.run(Secret)