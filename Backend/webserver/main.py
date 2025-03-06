from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import utilities
import json
app = FastAPI()

origins = ["*"]

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
def chatbot(conversation_id: str, message: str):
    context = []
    connection = utilities.connectDB()
    cursor = connection.cursor()

    if conversation_id is not None and conversation_id != "":
        result = utilities.selectQuery(cursor, conversation_id)

        if result is None:
            return {"message": "The conversation id doesn't exist."}
        conversation_id, context = result
        context = json.loads(context)

    response = utilities.callChatBot(message, context)
    context += [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response},
    ]

    if conversation_id is None or conversation_id == "":
        conversation_id = utilities.generateUUID()
        utilities.insertQuery(cursor, conversation_id, json.dumps(context))
        connection.commit()
    else:
        utilities.updateQuery(cursor, conversation_id, json.dumps(context))
        connection.commit()

    utilities.disconnectDB(connection)
    utilities.updateKeyInDictionary(context, "content", "message")
    print({"conversation_id": {conversation_id}, "message": context})
    return {"conversation_id": {conversation_id}, "message": context}