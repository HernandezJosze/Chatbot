import ollama
import sys
import inspect
import os

script_directory = os.path.dirname(os.path.abspath(
  inspect.getfile(inspect.currentframe())))

sys.path.insert(1, script_directory + '/../')
import env
client = ollama.Client()

def isCustomModelCreated(custom_model: str):
    for model in client.list().models:
      if custom_model in model.model:
        return True
    return False

def createCustomOllamaModel(custom_model: str):
    client.create(
      model=custom_model,
      from_='dolphin-llama3:8b',
      system=env.ENV_OLLAMA_SYSTEM,
      stream=False,
      parameters={"temperature": 1},
    )

for model in client.list().models:
    if not isCustomModelCreated(env.ENV_OLLAMA_MODEL):
        createCustomOllamaModel(env.ENV_OLLAMA_MODEL)
questions = ["Mac es Mejor que windows",
             "En Mac no hay virus",
             "Pero Mac es mejor porque yo lo digo",
             "Creo que tienes razon"]
context = []
for question in questions:
    print("user: ", question)
    message = [{"role": "user", "content": question}]
    response = client.chat(
          model=env.ENV_OLLAMA_MODEL,
          messages = context + message,
    )
    context += message + [{"role": "assistant", "content": response.message.content}]
    print("chatbot: ", response.message.content)