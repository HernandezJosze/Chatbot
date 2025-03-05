from fastapi import FastAPI
import functions
app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello Worlds"}

@app.get("/chatbot")
def chatbot(id: str, message: str):
    context = ""
    connection = functions.connectDB()
    cursor = connection.cursor()

    if id is not None and id != "":
        result = functions.selectQuery(cursor, id)
        if result is not None:
            id, message = result
        context += message

    if id is None or id == "":
        id = functions.generateUUID()
        cursor.execute("INSERT INTO db_chatbot.t_conversation (id, conversation) VALUES (?, ?)", (id, message))
        context+= f"user: {message}"
        connection.commit()

    functions.disconnectDB(connection)
    return {"id": {id}, "message": context}
