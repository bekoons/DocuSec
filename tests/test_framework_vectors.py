import sys
from pathlib import Path

# Ensure application modules are importable
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import framework_vectors


def test_build_framework_vectorstores(monkeypatch):
    sample = [
        {
            "framework_title": "ISO",
            "control_number": "1",
            "control_language": "Clause one. Clause two",
        },
        {
            "framework_title": "ISO",
            "control_number": "2",
            "control_language": "Another clause",
        },
        {
            "framework_title": "NIST",
            "control_number": "A",
            "control_language": "Alpha; Beta",
        },
    ]

    monkeypatch.setattr(framework_vectors, "fetch_controls", lambda db_path=None: sample)

    captured = {}

    def fake_embed(texts, metadatas=None):
        captured["texts"] = texts
        captured["metadatas"] = metadatas
        return {"texts": texts, "metadatas": metadatas}

    monkeypatch.setattr(framework_vectors, "embed_and_store", fake_embed)

    stores = framework_vectors.build_framework_vectorstores()

    assert set(stores.keys()) == {"ISO", "NIST"}

    iso = stores["ISO"]
    assert iso["texts"] == ["Clause one", "Clause two", "Another clause"]
    assert iso["metadatas"] == [
        {"framework": "ISO", "section_id": "1"},
        {"framework": "ISO", "section_id": "1"},
        {"framework": "ISO", "section_id": "2"},
    ]

    nist = stores["NIST"]
    assert nist["texts"] == ["Alpha", "Beta"]
    assert nist["metadatas"] == [
        {"framework": "NIST", "section_id": "A"},
        {"framework": "NIST", "section_id": "A"},
    ]

