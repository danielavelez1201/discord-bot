from os import listdir
from os.path import isfile, join
from config import cursor, cnx, delimiter
from mysql.connector import Error


def generate_from_csv():
    tables = [
        "servers",
        "users",
        "users_servers",
        "keywords",
        "messages",
        "questions",
        "answers",
        "keywords_messages",
        "keywords_questions",
        "keywords_answers",
    ]
    for table in tables:
        with open("data/" + table + ".csv", "r") as table_data:
            header, *rows = table_data.readlines()
        col_names = [name.strip() for name in header.split(delimiter)]
        col_sql = "(" + ",".join(col_names) + ")"
        rows_sql = []
        for row in rows:
            row_values = [value.strip() for value in row.split(delimiter)]
            row_sql = "(" + ",".join(row_values) + ")"
            rows_sql.append(row_sql)
        insert_sql = "INSERT IGNORE INTO {} {} VALUES {}".format(
            table, col_sql, ",".join(rows_sql)
        )
        try:
            cursor.execute(insert_sql)
            cnx.commit()
            print(table, "DONE")
        except Error as err:
            print("Tried adding answer: {}".format(err))
    return


generate_from_csv()
