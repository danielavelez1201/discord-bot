from re import I
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from utils.gpt3 import *
from db.functions.db_fetch import *
from db.functions.db_update import *
from utils.helpers import *
from similar_questions import ask_question_suggestions

with open("answers.txt", "r") as secrets_file:
    secret = secrets_file.read()
    print(secret)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="", intents=intents)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    id = msg.id
    author = msg.author
    server = msg.author.guild
    text = msg.content

    addServer(server.id, server.name, server.member_count)
    addUser(author.id, author.name, author.nick, server.id)
    addMessage(id, author.id, server.id, text, 0)


@slash.slash(
    name="summary", description="Ask a Question!", guild_ids=[966704306235519118]
)
async def summary(ctx):
    result = messagesFormatted()
    await ctx.send(result)


@slash.slash(
    name="rankings",
    description="See Contributor Rankings!",
    guild_ids=[966704306235519118],
    options=[
        create_option(
            name="count",
            description="Count",
            option_type=4,
            required=True,
        ),
    ],
)
async def rankings(ctx, count):
    contributors = get_top_contributors(count)
    count = 0
    result = "Rankings:\n"
    for (id, name, nick, contribution_score) in contributors:
        count += 1
        if contribution_score == 0:
            await ctx.send(result)
            return
        nick = "(" + nick + ")" if nick != None else ""
        result += f"{count}) {name}{nick}: {str(contribution_score)}\n"
    await ctx.send(result)


@bot.event
async def on_raw_reaction_add(payload):
    addServer(
        payload.guild_id, payload.member.guild.name, payload.member.guild.member_count
    )
    addUser(
        payload.user_id, payload.member.name, payload.member.nick, payload.guild_id
    )
    # Toggle accepted and answered if reacted to answer
    if payload.emoji.name == "✅":
        (answer, question) = get_answer_question_from_answer_id(
            payload.message_id
        )
        current_user = payload.user_id
        if (
            answer
            and question
            and current_user == question["author_id"]
            and current_user != answer["author_id"]
        ):
            acceptAnswer(question["id"], answer["id"])

    # Increment contributor score
    msg_user_id = get_user_id_from_message_id(payload.message_id)
    if len(msg_user_id) > 0:
        print(msg_user_id)
        msg_user_id = msg_user_id[0]
        current_contribution_score = get_score_from_author(msg_user_id)[0][0]
        addContribution(
            (0 if current_contribution_score == None else current_contribution_score)
            + 1,
            msg_user_id,
        )

@slash.slash(
    name="ask_question",
    description="Ask a Question!",
    guild_ids=[966704306235519118],
    options=[
        create_option(
            name="title",
            description="Question Title",
            option_type=3,
            required=True,
        ),
        create_option(
            name="question_body",
            description="Question Body",
            option_type=3,
            required=True,
        ),
        create_option(
            name="bounty",
            description="Bounty",
            option_type=4,
            required=False,
        ),
    ],
)

async def ask_question(ctx, title, question_body, bounty=0, include_bounty=False):    
    addServer(
        ctx.guild_id, ctx.author.guild.name, ctx.author.guild.member_count
    )
    addUser(ctx.author_id, ctx.author.name, ctx.author.nick, ctx.guild_id)

    question_suggestions = ''
    keywords = []
    question_id = '000'

    db_recording_on = True
    if db_recording_on:
        question_id = add_question(ctx.author_id, ctx.guild_id, title, question_body, bounty, 0, 0)

    bounty_str = f'Bounty of {bounty}\n' if include_bounty else ''
    message = await ctx.send(
        f"""\n**{title}**\n{question_body}\n{bounty_str}
🔮 To respond to this question, add #{question_id}"""
    )
    print(message)
    if db_recording_on:
        update_question_message_id(question_id, message.id)

    gpt3_on = True
    if gpt3_on:
        keywords = extract_keywords(question_body)
        question_suggestions = ask_question_suggestions(keywords, gpt3_on)
        print('question suggestions:', question_suggestions)
    
    if db_recording_on:
        add_keywords(question_id, keywords)

    await ctx.send(
        f"""
        {question_suggestions} \n
        """
    )

@slash.slash(
    name="answer",
    description="Answer a Question!",
    guild_ids=[966704306235519118],
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
    addServer(
        ctx.guild_id, ctx.author.guild.name, ctx.author.guild.member_count
    )
    addUser(ctx.author_id, ctx.author.name, ctx.author.nick, ctx.guild_id)
    keyword = "apple"
    addKeyword(keyword)
    sent_message = await ctx.send(
        "Answering Question with Id{}\n{}".format(question_id, answer_body)
    )
    addAnswer(
        sent_message.id,
        ctx.author_id,
        question_id,
        ctx.guild_id,
        answer_body,
        0,
        0,
        keyword,
    )


# TBD: What do we do if a user wants to attach an existing post to a question
# @slash.slash(
#     name="attach_answer",
#     description="Attach an Answer to a Question",
#     guild_ids=[967824448365412462],
#     options=[
#         create_option(
#             name="question_id",
#             description="Question Id",
#             option_type=3,
#             required=True,
#         ),
#         create_option(
#             name="post",
#             description="Search for a Post You Made",
#             option_type=3,
#             required=True,
#         ),
#     ],
# )
# async def attach_answer(ctx, question_id, answer_body):
#     db_update.addServer(
#         ctx.guild_id, ctx.author.guild.name, ctx.author.guild.member_count
#     )
#     db_update.addUser(ctx.author_id, ctx.author.name, ctx.author.nick, ctx.guild_id)
#     keyword = "apple"
#     db_update.addKeyword(keyword, ctx.guild_id)
#     await ctx.send("Attaching to Question#{}: {}".format(question_id, answer_body))


bot.run(secret)


