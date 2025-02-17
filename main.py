"""RAG on Codebase with py, cpp, md files using Langchain."""

import sys
import time
import warnings

from rag import (
    compile_and_get_graph
)
from vectorize import (
    vectorize_codebase
)


# Ignore all warnings
warnings.filterwarnings("ignore")

# Vectorize codebase, Note: controlled by env variable
vectorize_codebase()

# Setup RAG graph
graph = compile_and_get_graph()


# Function to run RAG
while True:
    # Ignore empty queries
    query = None
    print("\n\n======================================")
    while not query:
        query = input("\nEnter query: ")

    if query == "exit" or query == "quit":
        sys.exit(0)

    print("\n======================================\n")
    try:
        for message, metadata in graph.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="messages"
        ):
            # Terminal users deserve some pretty printing of the response
            for char in message.content:
                print(char, end="", flush=True)
                time.sleep(0.01)
    except Exception as e:
        print(f'Error in RAG {str(e)}')
