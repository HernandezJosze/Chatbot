import mariadb
import sys
import uuid
import env
import requests
import json
import ollama

client = ollama.Client(host=env.ENV_CONFIG_OLLAMA_HOST)


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
        cursor.execute("SELECT id, conversation from t_conversation WHERE id=?;", (id,))
        return cursor.fetchone()
    except mariadb.Error as e:
        print(f"Error: {e}")

def insertQuery(cursor, id: str, msg: str):
    try:
        cursor.execute("INSERT INTO t_conversation (id, conversation) VALUES (?, ?);", (id, msg))
    except mariadb.Error as e:
        print(f"Error: {e}")

def updateQuery(cursor, id: str, msg: str):
    try:
        cursor.execute("UPDATE t_conversation SET conversation=? WHERE id=?;", (msg, id))
    except mariadb.Error as e:
        print(f"Error: {e}")

# User must ensure the new_key is not already a key in the dictionary.
def updateKeyInDictionary(collection: list, old_key, new_key):
    for dict in collection:
        dict[new_key] = dict.pop(old_key)

def isCustomModelCreated(custom_model: str):
    for model in client.list().models:
      if custom_model in model.model:
        return True
    return False

def createCustomOllamaModel(custom_model: str):
    client.create(
      model=custom_model,
      from_='llama3.2',
      system=env.CONFIG_OLLAMA_SYSTEM,
      stream=False,
      parameters={"temperature": 1},
    )

def callChatBot(message, context):
    if not isCustomModelCreated(env.ENV_OLLAMA_MODEL):
        print("Creating custom model")
        createCustomOllamaModel(env.ENV_OLLAMA_MODEL)

    response = client.chat(
        model=env.ENV_OLLAMA_MODEL,
        messages= context + [{"role": "user", "content": message}],
    )
    return response.message.content