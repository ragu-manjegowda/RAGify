"""RAG on Codebase with py, cpp, md files using Langchain."""

import re
import sys
import time
import warnings

from rag import (
    compile_and_get_graph
)
from utils import (
    print_line_with_newline,
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
    print_line_with_newline()

    # Ignore empty queries
    query = None
    while not query:
        query = input("User:\n")

    # Exit
    if query == "exit" or query == "quit" or query == "q":
        sys.exit(0)

    print_line_with_newline()

    try:
        print("Chatbot:")
        for message, metadata in graph.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="messages"
        ):
            if metadata['langgraph_step'] == 2:
                # Regular expression to match source paths
                # (i.e., the string inside 'source': '...')
                pattern = re.compile(r"'source':\s*'([^']+)'")

                # Find all matches for the pattern
                file_paths = pattern.findall(message.content)

                print(f"\nContext: {file_paths}")
                print_line_with_newline()

            else:
                # Terminal users deserve some pretty printing of the response
                for char in message.content:
                    print(char, end="", flush=True)
                    time.sleep(0.01)

    except Exception as e:
        print(f'Error in RAG {str(e)}')
