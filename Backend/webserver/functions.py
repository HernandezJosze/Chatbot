import mariadb
import sys
import uuid
import env
from ollama import chat

def connectDB():
    try:
        conn = mariadb.connect(
            user=env.ENV_DB_USER,
            password=env.ENV_DB_PASSWORD,
            host=env.ENV_DB_HOST,
            port=3306,
            database=env.ENV_DB_DATABASE
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

def disconnectDB(connection):
    try:
        connection.close()

    except mariadb.Error as e:
        print(f"!Error disconnecting from MariaDB Platform: {e}")
        sys.exit(1)

def generateUUID() -> str:
    return str(uuid.uuid4())

def selectQuery(cursor, id: str):
    try:
        cursor.execute("SELECT id, conversation from db_chatbot.t_conversation where id=?;", (id,))
        return cursor.fetchone()
    except mariadb.Error as e:
        print(f"Error: {e}")

def callChatBot(message, context):
    return ""