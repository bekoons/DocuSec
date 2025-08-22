from typing import List

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


def embed_and_store(texts: List[str]):
    """Create embeddings for text chunks and store them in a FAISS vector store."""
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts, embeddings)
    return vectorstore

