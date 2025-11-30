#!/usr/bin/env bash

# I used an LLM to help come up with this bash script
MODEL_NAME="${OLLAMA_MODEL:-llama2}"

ollama serve &
pid=$!

# Wait for server to be reachable
until curl -s http://localhost:11434/api/tags > /dev/null; do
  echo "Waiting for Ollama to start..."
  sleep 2
done

# Pull model if not already available
if ! curl -s http://localhost:11434/api/tags | grep -q "\"name\":\"${MODEL_NAME}\""; then
  echo "Pulling model: ${MODEL_NAME}..."
  ollama pull "${MODEL_NAME}"
else
  echo "Model '${MODEL_NAME}' already pulled."
fi

echo "Ollama server and model ready. Keeping container running..."
wait $pid