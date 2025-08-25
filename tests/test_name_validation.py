import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

import app.embeddings as emb
from app.validation import validate_policy_name


class DummyStore:
    def __init__(self):
        self.saved = None

    def save_local(self, path: str) -> None:  # pragma: no cover - behaves like FAISS
        Path(path).mkdir(parents=True, exist_ok=True)
        self.saved = path


def test_save_vectorstore_sanitizes_name(tmp_path: Path):
    store = DummyStore()
    emb.save_vectorstore(store, "../PolicyB", base_dir=tmp_path)
    assert store.saved == str(tmp_path / "PolicyB")


def test_load_vectorstore_sanitizes_name(tmp_path: Path, monkeypatch):
    class DummyFAISS:
        @staticmethod
        def load_local(path, embeddings, allow_dangerous_deserialization=True):
            DummyFAISS.path = path
            return "loaded"

    monkeypatch.setattr(emb, "FAISS", DummyFAISS)
    monkeypatch.setattr(emb, "OpenAIEmbeddings", lambda: None)
    result = emb.load_vectorstore("../PolicyC", base_dir=tmp_path)
    assert result == "loaded"
    assert DummyFAISS.path == str(tmp_path / "PolicyC")


def test_validate_policy_name_valid_and_invalid():
    valid = ["Policy1", "Policy_A", "Policy-1"]
    invalid = ["../etc/passwd", "Policy name", "Policy$"]
    for name in valid:
        validate_policy_name(name)
    for name in invalid:
        with pytest.raises(ValueError):
            validate_policy_name(name)
