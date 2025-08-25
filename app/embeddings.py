"""Utilities for working with policy embeddings and vector stores."""

from __future__ import annotations

from typing import List, Dict, Any, BinaryIO
from pathlib import Path
import pickle

from .utils import trace

try:  # pragma: no cover - optional community dependency
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    import faiss
    from langchain_community.docstore.in_memory import InMemoryDocstore
    from langchain_core.documents.base import Document
except Exception:  # pragma: no cover - executed only when packages missing
    OpenAIEmbeddings = None  # type: ignore[assignment]
    FAISS = None  # type: ignore[assignment]
    faiss = None  # type: ignore[assignment]
    InMemoryDocstore = None  # type: ignore[assignment]
    Document = None  # type: ignore[assignment]


VECTORSTORE_DIR = Path("vector_store")


def embed_and_store(texts: List[str], metadatas: List[Dict[str, Any]] | None = None):
    """Create embeddings for text chunks and store them in a FAISS vector store."""

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
    """Persist a vector store to disk under a given name."""

    safe_name = Path(name).name
    path = Path(base_dir) / safe_name
    path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(path))


def list_vectorstores(base_dir: Path | str = VECTORSTORE_DIR) -> List[str]:
    """Return a sorted list of stored policy vector store names."""

    path = Path(base_dir)
    if not path.exists():
        return []
    return sorted([p.name for p in path.iterdir() if p.is_dir()])


def _safe_load_vectorstore_data(file_obj: BinaryIO):
    """Safely deserialize docstore and mapping using a restricted unpickler."""

    if InMemoryDocstore is None or Document is None:
        raise ImportError("LangChain community docstore classes are unavailable")

    class SafeUnpickler(pickle.Unpickler):  # type: ignore[misc]
        def find_class(self, module: str, name: str):  # noqa: D401
            allowed = {
                (
                    "langchain_community.docstore.in_memory",
                    "InMemoryDocstore",
                ): InMemoryDocstore,
                (
                    "langchain_core.documents.base",
                    "Document",
                ): Document,
            }
            if module == "builtins":
                import builtins

                return getattr(builtins, name)
            if (module, name) in allowed:
                return allowed[(module, name)]
            raise pickle.UnpicklingError(f"global '{module}.{name}' is forbidden")

    docstore, index_to_docstore_id = SafeUnpickler(file_obj).load()
    if not (
        isinstance(docstore, InMemoryDocstore)
        and isinstance(index_to_docstore_id, dict)
    ):
        raise ValueError("Unexpected data in vector store pickle")
    return docstore, index_to_docstore_id


def load_vectorstore(name: str, base_dir: Path | str = VECTORSTORE_DIR):
    """Load a previously saved vector store by name without unsafe pickle use."""

    if OpenAIEmbeddings is None or FAISS is None or faiss is None:
        raise ImportError("LangChain community embeddings/vectorstores are unavailable")

    safe_name = Path(name).name
    path = Path(base_dir) / safe_name
    embeddings = OpenAIEmbeddings()
    index = faiss.read_index(str(path / "index.faiss"))
    with open(path / "index.pkl", "rb") as f:
        docstore, index_to_docstore_id = _safe_load_vectorstore_data(f)
    return FAISS(embeddings, index, docstore, index_to_docstore_id)

