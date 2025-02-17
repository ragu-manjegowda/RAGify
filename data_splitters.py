"""Splitters for data loaded using Langchain."""

from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter
)


def split_cpp_files(cpp_docs):
    """Split C++ files into sub-documents."""
    cpp_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.CPP
    )

    cpp_splits = cpp_splitter.split_documents(cpp_docs)
    return cpp_splits


def split_md_files(md_docs):
    """Split Markdown files into sub-documents."""
    md_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN
    )

    markdown_splits = md_splitter.split_documents(md_docs)
    return markdown_splits


def split_python_files(py_docs):
    """Split Python files into sub-documents."""
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON
    )

    py_splits = python_splitter.split_documents(py_docs)
    return py_splits
