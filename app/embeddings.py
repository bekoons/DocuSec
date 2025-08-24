from typing import List

try:  # pragma: no cover - optional community dependency
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
except Exception:  # pragma: no cover - executed only when packages missing
    OpenAIEmbeddings = None  # type: ignore[assignment]
    FAISS = None  # type: ignore[assignment]


def embed_and_store(texts: List[str]):
    """Create embeddings for text chunks and store them in a FAISS vector store."""
    if OpenAIEmbeddings is None or FAISS is None:
        raise ImportError("LangChain community embeddings/vectorstores are unavailable")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts, embeddings)
    return vectorstore

