FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip3 install -r requirements.txt && pip install ollama && pip install load-dotenv

COPY . .

CMD uvicorn main:app --host=0.0.0.0 --reload