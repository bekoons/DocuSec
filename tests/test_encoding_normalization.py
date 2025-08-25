import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.ingestion import read_file
from app.utils import ensure_utf8


def test_read_file_detects_cp1252_encoding():
    text = "Smart quotes: “Hello” and euro sign €"
    data = text.encode("cp1252")
    assert read_file(data) == text


def test_ensure_utf8_normalizes_bytes():
    text = "Smart quotes: “Hello” and euro sign €"
    data = text.encode("cp1252")
    assert ensure_utf8(data) == text
