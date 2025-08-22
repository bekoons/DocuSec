from typing import List


def read_file(data: bytes) -> str:
    """Decode raw file bytes into text."""
    return data.decode("utf-8", errors="ignore")


def chunk_document(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Simple word-based chunking for documents."""
    words = text.split()
    chunks: List[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max(chunk_size - overlap, 1)
    return chunks

