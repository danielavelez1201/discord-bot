from config import cursor, delimiter


def convert_to_csv(table_name):
    cursor.execute("SHOW FULL COLUMNS FROM " + table_name)
    columns = cursor.fetchall()
    result = delimiter.join([col[0] for col in columns]) + "\n"
    cursor.execute("SELECT * FROM " + table_name)
    rows = cursor.fetchall()
    for row in rows:
        row = [str(element) if element else "" for element in row]
        result += delimiter.join(row) + "\n"
    with open("data/" + table_name + ".csv", "w") as f:
        f.write(result)


dbs = [
    # "servers",
    # "users",
    # "users_servers",
    # "keywords",
    "messages",
    # "keywords_messages",
    # "questions",
    # "keywords_questions",
    # "answers",
    # "keywords_answers",
]
for db in dbs:
    convert_to_csv(db)
