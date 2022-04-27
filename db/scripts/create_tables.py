from mysql.connector import Error

from config import cursor

create_server_table = """
    CREATE TABLE IF NOT EXISTS servers (
        id BIGINT,
        name VARCHAR(100),
        member_count INT,
        PRIMARY KEY (id)
    );
"""

create_user_table = """
    CREATE TABLE IF NOT EXISTS users (
        id BIGINT NOT NULL,
        name VARCHAR(100),
        nick VARCHAR(100),
        contribution_score BIGINT,
        server_id BIGINT,
        PRIMARY KEY (id),
        FOREIGN KEY (server_id) REFERENCES servers(id)
    );
"""

create_message_table = """
    CREATE TABLE IF NOT EXISTS messages (
        id BIGINT NOT NULL,
        author_id BIGINT,
        server_id BIGINT,
        text VARCHAR(2000),
        upvotes BIGINT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY (author_id) REFERENCES users(id),
        FOREIGN KEY (server_id) REFERENCES servers(id)
    );
"""

create_keyword_table = """
    CREATE TABLE IF NOT EXISTS keywords (
        word VARCHAR(255) NOT NULL,
        server_id BIGINT,
        PRIMARY KEY (word),
        FOREIGN KEY (server_id) REFERENCES servers(id)
    );
"""

create_question_table = """
    CREATE TABLE IF NOT EXISTS questions (
        id BIGINT NOT NULL AUTO_INCREMENT,
        author_id BIGINT,
        server_id BIGINT,
        title VARCHAR(2000),
        body VARCHAR(2000),
        bounty BIGINT,
        upvotes BIGINT,
        answered BIT,
        keyword VARCHAR(255),
        PRIMARY KEY (id),
        FOREIGN KEY (author_id) REFERENCES users(id),
        FOREIGN KEY (server_id) REFERENCES servers(id),
        FOREIGN KEY (keyword) REFERENCES keywords(word)
    );
"""

create_answer_table = """
    CREATE TABLE IF NOT EXISTS answers (
        id BIGINT NOT NULL,
        author_id BIGINT,
        question_id BIGINT,
        server_id BIGINT,
        body VARCHAR(2000),
        upvotes BIGINT,
        accepted BIT,
        keyword VARCHAR(255),
        PRIMARY KEY (id),
        FOREIGN KEY (author_id) REFERENCES users(id),
        FOREIGN KEY (question_id) REFERENCES questions(id),
        FOREIGN KEY (server_id) REFERENCES servers(id),
        FOREIGN KEY (keyword) REFERENCES keywords(word)
    );
"""

try:
    cursor.execute(create_server_table)
    cursor.execute(create_user_table)
    cursor.execute(create_message_table)
    cursor.execute(create_keyword_table)
    cursor.execute(create_question_table)
    cursor.execute(create_answer_table)
except Error as err:
    print("Something went wrong: {}".format(err))
