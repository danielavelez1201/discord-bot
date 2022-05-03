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
        try:
            with open("../../data/" + table + ".csv", "r") as table_data:
                header, *rows = table_data.readlines()
            col_names = [name.strip() for name in header.split(delimiter)]
            col_sql = "(" + ",".join(col_names) + ")"
            value_slots = ", ".join(["%s" for i in range(len(col_names))])
            for row in rows:
                row_values = [value.strip() for value in row.split(delimiter)]
                insert_sql = "INSERT IGNORE INTO {} {} VALUES ({})".format(
                    table, col_sql, value_slots
                )
                try:
                    cursor.execute(insert_sql, row_values)
                    cnx.commit()
                    print(table, "DONE")
                except Error as err:
                    print("Tried adding answer: {}".format(err))
        except Error as err:
            print('skipped because of: ', err)
    return


generate_from_csv()
