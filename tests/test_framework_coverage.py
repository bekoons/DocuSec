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


class DummyMetaDoc:
    def __init__(self, metadata):
        self.page_content = ""
        self.metadata = metadata


class DummyMetaStore:
    def __init__(self) -> None:
        self.queries = []

    def similarity_search(self, query: str, k: int = 4):
        self.queries.append((query, k))
        return [DummyMetaDoc({"text": f"text for {query}"})]


def test_check_framework_coverage_metadata_text():
    store = DummyMetaStore()
    controls = [
        {
            "framework_title": "ISO",
            "control_number": "1",
            "control_language": "Requirement text",
        }
    ]
    results = check_framework_coverage(store, controls, k=1)
    assert results[0]["policy_excerpts"] == ["text for Requirement text"]
    assert store.queries == [("Requirement text", 1)]


class DummyScoreStore:
    def __init__(self) -> None:
        self.queries = []

    def similarity_search_with_relevance_scores(self, query: str, k: int = 4):
        self.queries.append((query, k))
        return [
            (DummyDoc(f"low1: {query}"), 0.1),
            (DummyDoc(f"high1: {query}"), 0.9),
            (DummyDoc(f"low2: {query}"), 0.2),
            (DummyDoc(f"mid: {query}"), 0.5),
            (DummyDoc(f"high2: {query}"), 0.8),
        ]


def test_check_framework_coverage_limits_and_ranks():
    store = DummyScoreStore()
    controls = [
        {
            "framework_title": "ISO",
            "control_number": "1",
            "control_language": "Requirement text",
        }
    ]
    results = check_framework_coverage(store, controls, k=5)
    assert results[0]["policy_excerpts"] == [
        "high1: Requirement text",
        "high2: Requirement text",
        "mid: Requirement text",
    ]
    assert store.queries == [("Requirement text", 5)]
