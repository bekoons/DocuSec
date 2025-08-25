from typing import List, Dict, Any

try:  # pragma: no cover - optional community dependency
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
except Exception:  # pragma: no cover - executed only when packages missing
    OpenAIEmbeddings = None  # type: ignore[assignment]
    FAISS = None  # type: ignore[assignment]


def embed_and_store(texts: List[str], metadatas: List[Dict[str, Any]] | None = None):
    """Create embeddings for text chunks and store them in a FAISS vector store.

    Args:
        texts: The textual chunks to embed.
        metadatas: Optional list of metadata dictionaries to associate with each
            text.  When provided, the metadata at index ``i`` will be stored
            alongside ``texts[i]`` in the resulting vector store.

    Returns:
        A FAISS vector store containing the embedded texts and their metadata.
    """
    if OpenAIEmbeddings is None or FAISS is None:
        raise ImportError("LangChain community embeddings/vectorstores are unavailable")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    return vectorstore

