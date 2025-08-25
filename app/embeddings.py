from typing import List, Dict, Any
from pathlib import Path

from .utils import trace

try:  # pragma: no cover - optional community dependency
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
except Exception:  # pragma: no cover - executed only when packages missing
    OpenAIEmbeddings = None  # type: ignore[assignment]
    FAISS = None  # type: ignore[assignment]

VECTORSTORE_DIR = Path("vector_store")


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
    with trace(
        "embeddings.embed_and_store",
        inputs={"texts": texts, "metadatas": metadatas},
    ):
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    return vectorstore


def save_vectorstore(
    vectorstore: Any, name: str, base_dir: Path | str = VECTORSTORE_DIR
) -> None:
    """Persist a vector store to disk under a given name.

    Args:
        vectorstore: The FAISS vector store instance to persist.
        name: Identifier for the stored policy.
        base_dir: Directory where policy vector stores are maintained.
    """

    path = Path(base_dir) / name
    path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(path))


def list_vectorstores(base_dir: Path | str = VECTORSTORE_DIR) -> List[str]:
    """Return a sorted list of stored policy vector store names."""

    path = Path(base_dir)
    if not path.exists():
        return []
    return sorted([p.name for p in path.iterdir() if p.is_dir()])


def load_vectorstore(name: str, base_dir: Path | str = VECTORSTORE_DIR):
    """Load a previously saved vector store by name."""

    if OpenAIEmbeddings is None or FAISS is None:
        raise ImportError(
            "LangChain community embeddings/vectorstores are unavailable"
        )
    path = Path(base_dir) / name
    embeddings = OpenAIEmbeddings()
    # Explicitly disable dangerous deserialization to avoid executing
    # arbitrary code when loading persisted vector stores.
    return FAISS.load_local(
        str(path), embeddings, allow_dangerous_deserialization=False
    )

