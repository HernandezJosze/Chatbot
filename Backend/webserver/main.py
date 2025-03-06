from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import utilities
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
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                        detail="Esta funcionalidad aún no está implementada")

@app.post("/chatbot")
def chatbot(id: str, message: str):
    context = []
    connection = utilities.connectDB()
    cursor = connection.cursor()

    if id is not None and id != "":
        result = utilities.selectQuery(cursor, id)

        if result is None:
            return {"message": "The conversation id doesn't exist."}
        id, context = result
        context = json.loads(context)

    response = utilities.callChatBot(message, context)
    context += [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response},
    ]

    if id is None or id == "":
        id = utilities.generateUUID()
        utilities.insertQuery(cursor, id, json.dumps(context))
        connection.commit()
    else:
        utilities.updateQuery(cursor, id, json.dumps(context))
        connection.commit()

    utilities.disconnectDB(connection)
    utilities.updateKeyInDictionary(context, "content", "message")
    return {"conversation_id": {id}, "message": context}