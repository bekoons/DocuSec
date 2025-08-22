"""FastAPI backend exposing document ingestion and query endpoints.

This module wires existing helper functions into HTTP endpoints consumed by
the Streamlit frontend.  Each endpoint includes basic documentation and notes
on security considerations.
"""

from __future__ import annotations

from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.control_mapper import map_controls
from app.embeddings import SimpleVectorStore, build_vector_store
from app.framework_loader import load_frameworks
from app.ingestion import parse_document
from app.rag_pipeline import answer_query


app = FastAPI(title="DocuSec API")

# In-memory state used for demonstration purposes only.  A production system
# should persist data and enforce authentication/authorization.
_chunks: List[str] = []
_store: SimpleVectorStore | None = None


class _UploadWrapper:
    """Adapter giving :func:`parse_document` a sync interface.

    FastAPI's :class:`~fastapi.UploadFile` exposes an async ``read`` method.
    ``parse_document`` expects a file-like object with a synchronous ``read``
    and ``name`` attribute.  This wrapper bridges that gap.
    """

    def __init__(self, name: str, data: bytes) -> None:
        self.name = name
        self._data = data

    def read(self) -> bytes:  # pragma: no cover - trivial
        return self._data


@app.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)) -> dict:
    """Ingest uploaded documents and build an in-memory vector store.

    Created for Streamlit frontend integration.

    Security considerations
    -----------------------
    * Assumes callers are authenticated; add proper auth before deployment.
    * Files are processed in-memory without antivirus scanning.  Validate file
      size and type to avoid malware or resource-exhaustion attacks.
    * Parsed text is stored globally in-process and is not encrypted.
    """

    global _chunks, _store
    for f in files:
        data = await f.read()
        wrapper = _UploadWrapper(f.filename, data)
        _chunks.extend(parse_document(wrapper))
    _store = build_vector_store(_chunks)
    return {"chunks": len(_chunks)}


@app.get("/frameworks")
def get_frameworks() -> dict:
    """Return the list of supported security frameworks.

    Security considerations
    -----------------------
    * Framework data is loaded from disk without validation.  Protect the
      underlying files from tampering and validate contents in production.
    """

    return {"frameworks": load_frameworks()}


class MappingRequest(BaseModel):
    framework: str


@app.post("/map_controls")
def map_controls_endpoint(req: MappingRequest) -> List[dict]:
    """Map ingested document chunks to framework controls.

    This endpoint was created for Streamlit functionality.

    Security considerations
    -----------------------
    * Requires prior document ingestion; otherwise returns ``400``.
    * Output includes raw document excerpts.  Apply access controls and scrub
      sensitive information before exposing in production.
    """

    if not _chunks:
        raise HTTPException(status_code=400, detail="No documents ingested")
    return map_controls(_chunks, req.framework)


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def query_endpoint(req: QueryRequest) -> dict:
    """Answer a user query using the previously built vector store.

    This endpoint was created for Streamlit functionality.

    Security considerations
    -----------------------
    * Returns ``400`` if no documents have been ingested.
    * ``query`` is used verbatim in substring searches; sanitize or log
      carefully to avoid injection and information-disclosure risks.
    """

    if _store is None:
        raise HTTPException(status_code=400, detail="No documents ingested")
    return {"answer": answer_query(req.query, _store)}

