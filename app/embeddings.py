from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class SimpleVectorStore:
    """A lightweight in-memory vector store using substring search.

    Security considerations
    -----------------------
    * Stored chunks are kept in plain text and in process memory; do not use
      this implementation for sensitive or regulated data without additional
      protections such as encryption at rest.
    * No access control is enforced.  Ensure callers are authorized to query
      the data contained within ``chunks``.
    """

    chunks: List[str]

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """Return up to ``top_k`` chunks containing the query string.

        Security considerations
        -----------------------
        * The search performs a simple case-insensitive substring match and
          does not sanitize ``query``.  Validate or sanitize user-provided
          input if it will be logged or persisted elsewhere.
        * ``top_k`` should be bounded to prevent excessive memory usage or
          denial-of-service scenarios.
        """
        results = [c for c in self.chunks if query.lower() in c.lower()]
        return results[:top_k]


def build_vector_store(chunks: List[str]) -> SimpleVectorStore:
    """Create a :class:`SimpleVectorStore` from text chunks.

    Security considerations
    -----------------------
    * Input ``chunks`` are accepted as-is.  Sanitize or strip sensitive data
      before building the store.
    """
    return SimpleVectorStore(chunks=chunks)
