from typing import Dict, List, Any


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
    k: int = 4,
) -> List[Dict[str, Any]]:
    """Return policy excerpts that may satisfy each control's requirements.

    Args:
        vectorstore: Vector store containing policy document embeddings.
        controls: List of control dictionaries belonging to a framework.
        k: Number of similar chunks to retrieve for each control.

    Returns:
        A list where each item represents a control with possible policy
        excerpts that address it. Each item contains the ``framework_title``,
        ``control_number``, ``control_language`` and a list of
        ``policy_excerpts`` strings.
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

    results: List[Dict[str, Any]] = []
    for control in controls:
        excerpts: List[str] = []
        if vectorstore is not None:
            try:
                docs = vectorstore.similarity_search(
                    control["control_language"], k=k
                )
                excerpts = [_get_text(doc) for doc in docs]
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


