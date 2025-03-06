import mariadb
import sys
import uuid
import env
import requests
import json
import ollama

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
        print(f"Error disconnecting from MariaDB Platform: {e}")
        sys.exit(1)

def generateUUID() -> str:
    return str(uuid.uuid4())

def selectQuery(cursor, id: str):
    try:
        cursor.execute("SELECT id, conversation from db_chatbot.t_conversation WHERE id=?;", (id,))
        return cursor.fetchone()
    except mariadb.Error as e:
        print(f"Error: {e}")

def insertQuery(cursor, id: str, msg: str):
    try:
        cursor.execute("INSERT INTO db_chatbot.t_conversation (id, conversation) VALUES (?, ?);", (id, msg))
    except mariadb.Error as e:
        print(f"Error: {e}")

def updateQuery(cursor, id: str, msg: str):
    try:
        cursor.execute("UPDATE db_chatbot.t_conversation SET conversation=? WHERE id=?;", (msg, id))
    except mariadb.Error as e:
        print(f"Error: {e}")

def callChatBot(message, context):
    client = ollama.Client(host=env.ENV_CONFIG_OLLAMA_HOST)
    check = context + [{"role": "user", "content": message}]
    print("check: ",check)
    response = client.chat(
        'llama3.2',
        messages= context+ [{"role": "user", "content": message}],
    )
    return response.message.content