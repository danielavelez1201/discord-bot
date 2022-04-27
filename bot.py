import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import db_fetch
import db_update

# import gpt3

with open("answers.txt", "r") as secrets_file:
    secret = secrets_file.read()

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

    db_update.addServer(server.id, server.name, server.member_count)
    db_update.addUser(author.id, author.name, author.nick, server.id)
    db_update.addMessage(id, author.id, server.id, text, 0)


@slash.slash(
    name="summary", description="Ask a Question!", guild_ids=[967824448365412462]
)
async def summary(ctx):
    result = db_fetch.messagesFormatted()
    await ctx.send(result)


@slash.slash(
    name="rankings",
    description="See Contributor Rankings!",
    guild_ids=[967824448365412462],
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
    contributors = db_fetch.get_top_contributors(count)
    count = 0
    result = "Rankings:\n"
    for (id, name, nick, contribution_score) in contributors:
        nick = "(" + nick + ")" if nick != None else ""
        result += f"{count}) {name}{nick}: {str(contribution_score)}\n"
    await ctx.send(result)


@bot.event
async def on_raw_reaction_add(payload):
    db_update.addServer(
        payload.guild_id, payload.member.guild.name, payload.member.guild.member_count
    )
    db_update.addUser(
        payload.user_id, payload.member.name, payload.member.nick, payload.guild_id
    )
    # Toggle accepted and answered if reacted to answer
    answer_user_id = db_fetch.get_user_id_from_answer_id(payload.message_id)
    if len(answer_user_id) > 0:
        answer_user_id = answer_user_id[0][0]
        question_user_id = db_fetch.get_question_from_answer_id(payload.message_id)
        if len(question_user_id) > 0:
            question_user_id = question_user_id[0][0]
            if (
                question_user_id
                == payload.user_id
                # and question_user_id != answer_user_id
            ):
                question_id = db_fetch.get_question_id_from_answer_id(
                    payload.message_id
                )
                if len(question_id) > 0:
                    question_id = question_id[0][0]
                    db_update.acceptAnswer(question_id, payload.message_id)

    # Increment contributor score
    # TODO
    # Account for when user removes a emote/uses a different one to message
    msg_user_id = db_fetch.get_author_from_message(payload.message_id)
    if len(msg_user_id) > 0:
        msg_user_id = msg_user_id[0][0]
        current_contribution_score = db_fetch.get_score_from_author(msg_user_id)[0][0]
        db_update.addContribution(
            (0 if current_contribution_score == None else current_contribution_score)
            + 1,
            msg_user_id,
        )


# def similarQuestions(question_body, question_id):
#     keywords = gpt3.extract_keywords(question_body)
#     db_update.addKeywordsToDB(keywords)
#     db_update.addQuestionIDtoKeywords(question_id)
#     similar_question_ids = db_fetch.get_similar_question_ids(keywords)
#     return similar_question_ids


def askQuestionSuggestions(questionId):
    message_intro = "You might want to check these out:"
    db_result = db_fetch.messagesFormatted()
    message_end = f"\nTo respond to this question, add #{questionId}"
    return message_intro + db_result + message_end


@slash.slash(
    name="ask_question",
    description="Ask a Question!",
    guild_ids=[967824448365412462],
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
async def ask_question(ctx, title, question_body, bounty=0):
    db_update.addServer(
        ctx.guild_id, ctx.author.guild.name, ctx.author.guild.member_count
    )
    db_update.addUser(ctx.author_id, ctx.author.name, ctx.author.nick, ctx.guild_id)
    keyword = "apple"
    db_update.addKeyword(keyword)
    questionId = db_update.addQuestion(
        ctx.author_id, ctx.guild_id, title, question_body, bounty, 0, 0, keyword
    )
    # print(similarQuestions(question_body, questionId))
    await ctx.send(
        "\n{}\n{}\nBounty of {}\n{}".format(
            title, question_body, bounty, askQuestionSuggestions(questionId)
        )
    )


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
    db_update.addServer(
        ctx.guild_id, ctx.author.guild.name, ctx.author.guild.member_count
    )
    db_update.addUser(ctx.author_id, ctx.author.name, ctx.author.nick, ctx.guild_id)
    keyword = "apple"
    db_update.addKeyword(keyword)
    sent_message = await ctx.send(
        "Answering Question with Id{}\n{}".format(question_id, answer_body)
    )
    db_update.addAnswer(
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
