import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.embeddings import save_vectorstore, list_vectorstores


class DummyStore:
    def __init__(self):
        self.saved = None

    def save_local(self, path: str) -> None:  # pragma: no cover - behaves like FAISS
        Path(path).mkdir(parents=True, exist_ok=True)
        self.saved = path


def test_save_and_list_vectorstores(tmp_path: Path):
    store = DummyStore()
    save_vectorstore(store, "PolicyA", base_dir=tmp_path)
    assert store.saved == str(tmp_path / "PolicyA")
    assert list_vectorstores(base_dir=tmp_path) == ["PolicyA"]
