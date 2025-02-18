# Contextual Code Exploration for Developers

This project aims to build a Retrieval-Augmented Generation (RAG) model for codebases written in C++ and Python. It focuses on providing efficient, minimalistic, and portable solutions for developers to explore and interact with their codebases.

<p align="center"> <a href="./man/figures/RAGify.mp4" target="_blank"> High quality video of below GIF </a></p>

<p align="center"> <img src="man/figures/RAGify.gif" alt="Click above link for video" width="900" height="350" /> </p>


## Motivation

Existing RAG models typically focus on unstructured text and often require heavy dependencies and resources, such as large GUI applications that consume excessive RAM and CPU. I couldn't find a RAG model tailored for codebases written in C++ and Python that meets the following criteria:

* Minimalistic: No unnecessary dependencies or heavyweight applications.
* Portable: Easily save and load embeddings from disk.
* Structured Parsing: Uses TreeSitter for parsing the code into Syntax Trees, providing more relevant context for the model.


## How is it done?

Instead of treating files as unstructured text, this project parses C++, Python, and Markdown files into their corresponding Syntax Tree representations using TreeSitter. This structured parsing helps provide more accurate and relevant context for code generation tasks.

* C++ files: Parsed into C++ syntax trees.
* Python files: Parsed into Python syntax trees.
* Markdown files: Parsed into Markdown structure for documentation-based queries.

This method enhances the model’s understanding of the code and improves the quality of context retrieval.


## Why is it done?

* Onboarding Tool: This can be used as an onboarding tool for new developers, helping them to explore unfamiliar codebases with contextualized information.
* Codebase Exploration: Helps developers quickly explore large codebases by providing relevant information without needing to manually input context for each request.
* Contextualized Code Retrieval: The model retrieves contextualized code or documentation based on queries, minimizing the need for manual search and enhancing the development experience.


## Installation

>[!WARNING]
>Do not use Python 3.13 as TreeSitter has compatibility issues with this version.

To install the required dependencies, follow these steps:

```sh
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```


## Usage

Configuration options can be found in the `env.py` file.

>[!NOTE]
This tool currently works with NVIDIA endpoints only. If you're using an endpoint other than NVIDIA, modify the client instantiation in llm.py as needed.
After the initial run, set VECTORIZE_CODEBASE to False to prevent vectorizing the codebase every time.

To run the model:
```sh
python3 main.py
```

## Makefile Usage

You can also manage installation and usage via the provided `Makefile`:

```sh
# Activate the virtual environment
make activate

# Install the required dependencies
make install

# Run the model
make run

# Clean up (remove pycache and vector store)
make clean

# Deactivate the virtual environment
make deactivate
```


## Possible Enhancements

### Web App
Currently, this tool is a CLI application. However, it can easily be extended into a web application using simple wrappers like Streamlit or Flask.

### Optimization
There is room for optimization by using a hybrid retrieval approach. Instead of only sending embeddings to the model, this approach can retrieve the original content from files based on similarity results and pass that to the model, further improving the context retrieval.

### Memory
Implement support to store chat history in memory, enabling the model to remember previous conversations and restore the history during the next run, making the interaction more seamless and intelligent.
