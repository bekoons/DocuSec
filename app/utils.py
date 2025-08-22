from __future__ import annotations

from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks.

    Parameters
    ----------
    text: str
        Raw text to split.
    chunk_size: int, optional
        Size of each chunk.
    overlap: int, optional
        Number of characters to overlap between chunks.

    Security considerations
    -----------------------
    * The function does not limit input size; extremely large ``text`` values
      could exhaust memory.  Validate or cap ``chunk_size`` and input length in
      production environments.
    * ``text`` is processed verbatim.  Sanitize data if chunks will be
      persisted or displayed to users to mitigate injection risks.
    """
    chunks: List[str] = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
