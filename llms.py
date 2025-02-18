"""Generate various llm clients using Langchain."""

from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain_nvidia_ai_endpoints import (
    ChatNVIDIA,
    NVIDIAEmbeddings
)

import os

from env import VECTOR_STORE_PATH

llm_client = None
tokenizer = None
vectorStore = None


def create_or_get_llm_client():
    """Create or get the llm."""
    global llm_client
    if llm_client is None:
        try:
            llm_client = ChatNVIDIA(
                # model="nvdev/qwen/qwen2.5-coder-32b-instruct",
                model="nvdev/meta/llama-3.3-70b-instruct",
                # model="nvdev/deepseek-ai/deepseek-r1",
                api_key=os.environ["OPENAI_API_KEY"],
                temperature=0.6,
                top_p=0.7,
                max_tokens=4096,
            )
        except Exception as e:
            print(f'Error in create_or_get_llm {str(e)}')

    return llm_client


class vector_store_client:
    """Vector store client."""

    def __init__(self):
        """Create or get the vector store client."""
        global vectorStore
        if vectorStore is None:
            try:
                # Initialize the embeddings
                embeddings = NVIDIAEmbeddings(
                    model="nvdev/nvidia/llama-3.2-nv-embedqa-1b-v2",
                    api_key=os.environ["OPENAI_API_KEY"],
                    truncate="NONE",
                )

                vectorStore = Chroma(
                    embedding_function=embeddings,
                    persist_directory=VECTOR_STORE_PATH,
                    client_settings=Settings(anonymized_telemetry=False)
                )

            except Exception as e:
                print(f'Error in vector_store {str(e)}')

    def add_documents_to_vector_store_client(self,
                                             split_documents_with_metadata):
        """Add documents to the vector store client."""
        global vectorStore

        if vectorStore is not None:
            try:
                vectorStore.add_documents(
                    documents=split_documents_with_metadata)

            except Exception as e:
                print(f'Error in create_vector_store {str(e)}')
        else:
            print("Vector store client is not initialized.")

    def similarity_search(self, query, k=3):
        """Similarity search."""
        global vectorStore
        result = None

        if vectorStore is not None:
            try:
                result = vectorStore.similarity_search(query, k=k)

            except Exception as e:
                print(f'Error in similarity_search {str(e)}')
        else:
            print("Vector store client is not initialized.")

        return result


# def create_or_get_tokenizer():
#     """Create or get the tokenizer."""
#     global tokenizer
#     model = "nvdev/nvidia/llama-3.2-nv-embedqa-1b-v2"
#     tokenizer=AutoTokenizer.from_pretrained(model)
