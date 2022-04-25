
from socket import create_server
import mysql.connector

cnx = mysql.connector.connect(host="localhost",
    user="danielavelez1201@gmail.com",
    password="Lailabeth2000*", port="3306", 
    database="athena")
cursor = cnx.cursor()

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
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY (author_id) REFERENCES users(id),
        FOREIGN KEY (server_id) REFERENCES servers(id)
    );
    """

create_thread_table = """
    CREATE TABLE IF NOT EXISTS thread_messages (
        id BIGINT NOT NULL, 
        author_id BIGINT,
        server_id BIGINT,
        thread_id BIGINT,
        text VARCHAR(2000),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY (author_id) REFERENCES users(id),
        FOREIGN KEY (server_id) REFERENCES servers(id),
    );
    """
cursor = cnx.cursor()
try:
    cursor.execute (create_server_table)
    cursor.execute (create_user_table)
    cursor.execute (create_message_table)
except mysql.connector.Error as err:
  print("Something went wrong: {}".format(err))
