import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.ingestion import read_file


def test_read_file_detects_cp1252_encoding():
    text = "Smart quotes: “Hello” and euro sign €"
    data = text.encode("cp1252")
    assert read_file(data) == text
