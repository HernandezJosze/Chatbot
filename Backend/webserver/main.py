from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import functions
import json
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:63343",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "Hello Worlds"}

@app.get("/chatbot")
def chatbot(id: str, message: str):
    context = []
    connection = functions.connectDB()
    cursor = connection.cursor()

    if id is not None and id != "":
        result = functions.selectQuery(cursor, id)

        if result is None:
            return {"message": "The conversation id doesn't exist."}
        id, context = result
        context = json.loads(context)

    response = functions.callChatBot(message, context)
    context += [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response},
    ]

    if id is None or id == "":
        id = functions.generateUUID()
        functions.insertQuery(cursor, id, json.dumps(context))
        connection.commit()
    else:
        functions.updateQuery(cursor, id, json.dumps(context))
        connection.commit()

    functions.disconnectDB(connection)
    return {"conversation_id": {id}, "message": context}