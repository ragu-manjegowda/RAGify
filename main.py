"""RAG on Codebase with py, cpp, md files using Langchain."""

import time

from rag import (
    compile_and_get_graph
)
from vectorize import (
    vectorize_codebase
)


# Vectorize codebase, Note: controlled by env variable
vectorize_codebase()

# Setup RAG graph
graph = compile_and_get_graph()


# Function to run RAG
query = input("Enter query: ")

for message, metadata in graph.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="messages"
):
    # Terminal users deserve some pretty printing of the response
    for char in message.content:
        print(char, end="", flush=True)
        time.sleep(0.01)
