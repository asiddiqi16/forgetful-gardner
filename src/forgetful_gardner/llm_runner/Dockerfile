FROM ollama/ollama

# Install curl (Debian-based image)
RUN apt-get update && apt-get install -y curl

COPY ./src/pull-llm.sh /pull-llm.sh
RUN chmod +x /pull-llm.sh

ENTRYPOINT ["/pull-llm.sh"]