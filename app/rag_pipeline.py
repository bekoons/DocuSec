from __future__ import annotations

from .embeddings import SimpleVectorStore


def answer_query(query: str, store: SimpleVectorStore) -> str:
    """Return a rudimentary answer using relevant excerpts from the store.

    Security considerations
    -----------------------
    * The function assumes callers are authorized to search the ``store``.
      Implement authentication and access control before exposing this
      capability to end users.
    * ``query`` is used directly in substring searches.  Sanitize or validate
      user input if search terms will be logged or displayed to other users.
    """
    matches = store.search(query)
    if not matches:
        return "No relevant information found."
    joined = "\n".join(f"- {m}" for m in matches)
    return f"Relevant excerpts:\n{joined}"
