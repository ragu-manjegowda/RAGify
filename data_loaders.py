"""Load specific file types using Langchain."""

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser

import os
import glob

from env import REPO_PATH


def load_cpp_files():
    """Load cpp files from a directory."""
    cpp_docs = []
    try:
        cpp_loader = GenericLoader.from_filesystem(
            REPO_PATH,
            glob="**/*",
            suffixes=[".hpp", ".cpp", ".h", ".c"],
            parser=LanguageParser()
        )

        cpp_docs = cpp_loader.load()
    except Exception as e:
        print(f'Error in load_cpp_files {str(e)}')

    return cpp_docs


def load_md_files():
    """Load md files from a directory."""
    md_docs = []
    try:
        # Glob all files with .md extension under REPO_PATH
        md_files = glob.glob(os.path.join(REPO_PATH, "**/*.md"),
                             recursive=True)

        # Initialize the loader for Markdown files
        md_loader = UnstructuredMarkdownLoader(
            md_files,
            mode="elements",
            strategy="fast",
        )

        md_docs = md_loader.load()
    except Exception as e:
        print(f'Error in load_md_files {str(e)}')

    return md_docs


def load_python_files():
    """Load python files from a directory."""
    py_docs = []
    try:
        py_loader = GenericLoader.from_filesystem(
            REPO_PATH,
            glob="**/*",
            suffixes=[".py"],
            parser=LanguageParser(language="python")
        )

        py_docs = py_loader.load()
    except Exception as e:
        print(f'Error in load_python_files {str(e)}')

    return py_docs
