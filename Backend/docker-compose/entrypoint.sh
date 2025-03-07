#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 10

ollama pull dolphin-llama3:8b

# Wait for Ollama process to finish.
wait $pid