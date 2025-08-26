"""Utilities for mapping compliance controls to policy text."""

from difflib import SequenceMatcher
import re
from typing import Any, Dict, List


def map_controls(frameworks: Dict[str, Dict[str, str]], documents: List[str]) -> Dict[str, List[str]]:
    """Naive control mapping by substring matching of control text in documents."""
    mapping: Dict[str, List[str]] = {name: [] for name in frameworks}
    for name, controls in frameworks.items():
        for control_id, control_text in controls.items():
            for doc in documents:
                if control_text.lower() in doc.lower():
                    mapping[name].append(control_id)
                    break
    return mapping


def check_framework_coverage(
    vectorstore: Any,
    controls: List[Dict[str, str]],
    k: int = 8,
) -> List[Dict[str, Any]]:
    """Return up to three policy excerpts that may satisfy each control.

    Args:
        vectorstore: Vector store containing policy document embeddings.
        controls: List of control dictionaries belonging to a framework.
        k: Number of candidate chunks to retrieve for each control.

    Returns:
        A list where each item represents a control with possible policy
        excerpts that address it. Each item contains the ``framework_title``,
        ``control_number``, ``control_language`` and a list of up to three
        ``policy_excerpts`` strings ranked by relevance.
    """

    def _get_text(doc: Any) -> str:
        """Return the most human readable text from a retrieved document."""

        text = getattr(doc, "page_content", "") or ""
        if not text and hasattr(doc, "metadata"):
            meta = getattr(doc, "metadata") or {}
            if isinstance(meta, dict):
                text = meta.get("text", "") or meta.get("page_content", "")
        if not isinstance(text, str):  # Fallback to string representation
            text = str(text)
        return text

    def _extract_quote(control_lang: str, policy_text: str) -> str:
        """Return the most similar sentence from ``policy_text``.

        The search is purely string based to ensure the output is an exact
        excerpt from the policy document rather than an LLM interpretation.
        """

        sentences = re.split(r"(?<=[.!?])\s+", policy_text)
        best_sentence = policy_text.strip()
        best_ratio = 0.0
        control_lower = control_lang.lower()
        for sentence in sentences:
            ratio = SequenceMatcher(None, control_lower, sentence.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_sentence = sentence.strip()
        return best_sentence

    results: List[Dict[str, Any]] = []
    MAX_EXCERPTS = 3
    for control in controls:
        excerpts: List[str] = []
        if vectorstore is not None:
            try:
                docs = []
                if hasattr(vectorstore, "similarity_search_with_relevance_scores"):
                    doc_scores = vectorstore.similarity_search_with_relevance_scores(
                        control["control_language"], k=k
                    )
                    doc_scores.sort(key=lambda x: x[1], reverse=True)
                    docs = [doc for doc, _ in doc_scores[:MAX_EXCERPTS]]
                else:
                    docs = vectorstore.similarity_search(
                        control["control_language"], k=k
                    )[:MAX_EXCERPTS]
                excerpts = [
                    _extract_quote(control["control_language"], _get_text(doc))
                    for doc in docs
                ]
            except Exception:
                excerpts = []
        results.append(
            {
                "framework_title": control["framework_title"],
                "control_number": control["control_number"],
                "control_language": control["control_language"],
                "policy_excerpts": excerpts,
            }
        )
    return results


