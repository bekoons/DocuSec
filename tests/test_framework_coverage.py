import sys
from pathlib import Path

# Ensure application modules are importable
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.control_mapper import check_framework_coverage


class DummyDoc:
    def __init__(self, content: str) -> None:
        self.page_content = content


class DummyStore:
    def __init__(self) -> None:
        self.queries = []

    def similarity_search(self, query: str, k: int = 4):
        self.queries.append((query, k))
        return [DummyDoc(f"match: {query}")]


def test_check_framework_coverage():
    store = DummyStore()
    controls = [
        {
            "framework_title": "ISO",
            "control_number": "1",
            "control_language": "Requirement text",
        }
    ]
    results = check_framework_coverage(store, controls, k=1)
    assert results == [
        {
            "framework_title": "ISO",
            "control_number": "1",
            "control_language": "Requirement text",
            "policy_excerpts": ["match: Requirement text"],
        }
    ]
    assert store.queries == [("Requirement text", 1)]
