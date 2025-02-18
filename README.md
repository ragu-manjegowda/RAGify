# RAG with CPP and Python Codebase

This project aims to build a RAG model for codebase written in C++ and Python.

## Motivation

I couldn't find any RAG model for codebase written in C++ and Python that is
minimalistic (no extra dependencies, heavyweight GUI apps hogging the entire
RAM and CPU), portable (dump embeddings to disk and load them from anywhere)
and parse the files as structured text using TreeSitter.


## How is it done?
Instead of parsing the files as unstructured text, files falling into one of
the three categories namely C++ files, Python files and Markdown files are
parsed for SyntaxTree (using TreeSitter) thus providing more relevant context
to the users.

## Why is it done?
* This can be used as onboarding tool for new developers or as a codebase
exploration tool.
* This has a great potential of being able to provide contextualized
information to users without them having to manually provide the context
to the model.

## Installation

>[!WARNING] Do not use python 3.13 as tree-sitter is broken in that version.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Checkout `env.py` for configuration options.

>[!NOTE] This only works with NVIDIA endpoints, for endpoint other than
NVIDIA, modify the client instantiation in `llm.py` as needed.

>[!NOTE] Turn VECTORIZE_CODEBASE to False after first run.

```bash
python3 main.py
```

## Makefile

Installation and usage can be done using makefile.

```bash
make activate # to activate the virtual environment
make install # to install the requirements
make run # to run the model
make clean # to remove pycache and vector store
make deactivate # to deactivate the virtual environment
```

## Future Work

### Web App
* Currently this is a CLI tool, however it can be easily extended to a web app
by adding a simple wrapper like streamlit.

### Optimization
* This can be further optimized to use hybrid approach to retrieve the
context. Instead of sending just the embeddings to the model, it retrieves
the original file content based on the similarity result and shares that
with the model.

### Memory
* Add support to store chat history in memory and restore it on next run.
