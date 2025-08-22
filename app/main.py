from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from typing import List

from .ingestion import read_file, chunk_document
from .embeddings import embed_and_store
from .rag_pipeline import build_rag, answer_query
from .framework_loader import load_frameworks
from .control_mapper import map_controls as perform_control_mapping
from .ui import upload_form
from . import utils

app = FastAPI(title="DocuSec API")

# Global state for simple proof of concept
vectorstore = None
rag_chain = None
frameworks = load_frameworks()


# Root endpoint: return API health status
@app.get("/")
def root() -> dict:
    """Health check endpoint for the API."""
    return {"status": "ok"}


# Document ingestion endpoint: upload file, chunk, embed, build RAG
@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)) -> dict:
    """Upload a document, chunk it, embed it and build the RAG pipeline."""
    global vectorstore, rag_chain
    text = read_file(await file.read())
    chunks = chunk_document(text)
    vectorstore = embed_and_store(chunks)
    rag_chain = build_rag(vectorstore)
    return {"chunks": len(chunks)}


# RAG query endpoint: ask questions over ingested content
@app.post("/query")
async def query_rag(question: str) -> dict:
    """Query the RAG pipeline for an answer."""
    if rag_chain is None:
        return {"error": "RAG pipeline not initialized"}
    answer = answer_query(rag_chain, question)
    return {"answer": answer}


# Framework retrieval endpoint: list loaded security frameworks
@app.get("/frameworks")
def get_frameworks() -> dict:
    """Return the loaded security frameworks."""
    return frameworks


# Control mapping endpoint: map text passages to framework controls
@app.post("/map_controls")
async def map_controls(documents: List[str]) -> dict:
    """Map document text to controls in the loaded frameworks."""
    mapping = perform_control_mapping(frameworks, documents)
    return mapping


# UI endpoint: serve HTML upload form
@app.get("/ui/upload_form", response_class=HTMLResponse)
def get_upload_form() -> HTMLResponse:
    """Return a simple HTML upload form."""
    return HTMLResponse(upload_form())


# Utility endpoint: expose service health check
@app.get("/utils/health")
def utils_health() -> dict:
    """Utility endpoint for service health."""
    return utils.health()

