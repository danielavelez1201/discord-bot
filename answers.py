# import mysql.connector
import re
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

with open("answers.txt", "r") as secrets_file:
    secret = secrets_file.read()


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)
slash = SlashCommand(bot, sync_commands=True)
# cnx = mysql.connector.connect(
#     host="localhost",
#     user="athena-admin",
#     password="abc123",
#     port="3306",
#     database="athena",
# )
# cursor = cnx.cursor()


@slash.slash(
    name="answer",
    description="Answer a Question!",
    guild_ids=[967824448365412462],
    options=[
        create_option(
            name="question_id",
            description="Question Id",
            option_type=3,
            required=True,
        ),
        create_option(
            name="answer_body",
            description="Answer Body",
            option_type=3,
            required=True,
        ),
    ],
)
async def answer(ctx, question_id, answer_body):
    await ctx.send("Answering Question#{}: {}".format(question_id, answer_body))


@slash.slash(
    name="attach_answer",
    description="Attach an Answer to a Question",
    guild_ids=[967824448365412462],
    options=[
        create_option(
            name="question_id",
            description="Question Id",
            option_type=3,
            required=True,
        ),
        create_option(
            name="post",
            description="Search for a Post You Made",
            option_type=3,
            required=True,
        ),
    ],
)
async def attach_answer(ctx, question_id, post):
    await ctx.send("Attaching to Question#{}: {}".format(question_id, post))


# @bot.command(name="answer")
# async def Answer(ctx, questionId, *args):
#     print(ctx.args)
#     await ctx.send(questionId)
#     await ctx.send(" ".join(args))


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
    # request_sql = "SELECT * FROM messages"
    # cursor.execute(request_sql)
    # result = cursor.fetchall()
    await ctx.send("HI")


@bot.event
async def on_raw_reaction_add(payload):
    print(payload.user_id)
    print(payload.emoji.name)


@bot.event
async def on_message(msg):
    id = msg.id
    author = msg.author
    if msg.author.bot:
        return
    server = msg.author.guild
    text = msg.content
    channel = bot.get_channel(msg.channel.id)

    if re.match(r"^\$answer \d* ", msg.content):
        updated = re.sub(r"^\$answer \d* ", "", text)
        await channel.send(updated)
        reply_message = await bot.wait_for("message", timeout=15.0)
        await msg.delete()
        # try:
        # except asyncio.TimeoutError:
        #     await channel.send("You ran out of time to answer!")
        # else:
        #     if reply_message.content == "yes":
        #         await channel.send("You replied yes")
        #     else:
        #         await channel.send("You didn't reply yes.")
    # print(f"{server.id}, {server.name}, {server.member_count}")
    # print(f"{author.id}, {author.name}, {author.nick}, {server.id}")
    # print(f"{id}, {author.id}, {server.id}, {text}")
    print(text)


bot.run(secret)
