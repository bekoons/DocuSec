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
        def __init__(self, embeddings, index, docstore, index_to_docstore_id):
            self.args = (embeddings, index, docstore, index_to_docstore_id)

    class DummyFaissModule:
        @staticmethod
        def read_index(path):
            DummyFaissModule.path = path
            return "index"

    monkeypatch.setattr(emb, "FAISS", DummyFAISS)
    monkeypatch.setattr(emb, "faiss", DummyFaissModule)
    monkeypatch.setattr(emb, "OpenAIEmbeddings", lambda: "emb")
    monkeypatch.setattr(emb, "_safe_load_vectorstore_data", lambda f: ("doc", {}))

    target = tmp_path / "PolicyC"
    target.mkdir()
    (target / "index.pkl").write_bytes(b"0")

    result = emb.load_vectorstore("../PolicyC", base_dir=tmp_path)
    assert isinstance(result, DummyFAISS)
    assert DummyFaissModule.path == str(target / "index.faiss")


def test_validate_policy_name_valid_and_invalid():
    valid = ["Policy1", "Policy_A", "Policy-1"]
    invalid = ["../etc/passwd", "Policy name", "Policy$"]
    for name in valid:
        validate_policy_name(name)
    for name in invalid:
        with pytest.raises(ValueError):
            validate_policy_name(name)
