"""Utilities for building vector stores for compliance frameworks."""

from __future__ import annotations

import re
from typing import Dict, List, Any

from .db import fetch_controls
from .embeddings import embed_and_store


def _split_into_clauses(text: str) -> List[str]:
    """Split a control's language into atomic clauses.

    The implementation is intentionally lightweight; it breaks text on periods,
    semicolons and newlines while stripping whitespace.  Empty clauses are
    ignored.
    """

    parts = re.split(r"[.;\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def build_framework_vectorstores(db_path: str | None = None) -> Dict[str, Any]:
    """Create a vector store for each framework stored in the database.

    Each control is broken into atomic clauses which are embedded and stored
    with metadata describing the framework and the control (section) identifier.

    Args:
        db_path: Optional path to the frameworks database.  If not provided the
            default path from :func:`app.db.fetch_controls` is used.

    Returns:
        A mapping of framework name to its corresponding vector store.
    """

    controls = fetch_controls(db_path=db_path) if db_path else fetch_controls()
    grouped: Dict[str, List[tuple[str, Dict[str, str]]]] = {}
    for row in controls:
        framework = row["framework_title"]
        section_id = row["control_number"]
        clauses = _split_into_clauses(row["control_language"])
        for clause in clauses:
            grouped.setdefault(framework, []).append(
                (clause, {"framework": framework, "section_id": section_id})
            )

    stores: Dict[str, Any] = {}
    for framework, items in grouped.items():
        texts = [text for text, _ in items]
        metadata = [meta for _, meta in items]
        stores[framework] = embed_and_store(texts, metadata)
    return stores

