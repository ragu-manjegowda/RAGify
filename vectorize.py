"""Vectorize codebase."""

from data_loaders import (
    load_cpp_files,
    load_md_files,
    load_python_files
)
from data_splitters import (
    split_cpp_files,
    split_md_files,
    split_python_files
)
from env import (
    VECTORIZE_CODEBASE,
    VECTORIZE_FILE_TYPES
)
from llms import (
    vector_store_client
)


def load_and_split_files():
    """Load and split files."""
    splits = []
    for enum, file_type in enumerate(VECTORIZE_FILE_TYPES):
        if enum == 0:
            docs = load_cpp_files()
            print(f"Loaded {len(docs)} documents of type {file_type}.")
            splits.extend(split_cpp_files(docs))
        elif enum == 1:
            docs = load_md_files()
            print(f"Loaded {len(docs)} documents of type {file_type}.")
            splits.extend(split_md_files(docs))
        else:
            docs = load_python_files()
            print(f"Loaded {len(docs)} documents of type {file_type}.")
            splits.extend(split_python_files(docs))

    return splits


def vectorize_codebase():
    """Vectorize codebase."""
    if VECTORIZE_CODEBASE:
        split_documents = load_and_split_files()

        # Create vector store instance
        vs_client = vector_store_client()

        # Add documents to the vector store
        vs_client.add_documents_to_vector_store_client(split_documents)
