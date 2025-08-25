import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.ingestion import chunk_document


def test_chunk_document_splits_policies_into_paragraphs():
    text = (
        "Privacy Policy\nParagraph A1.\n\nParagraph A2.\n"
        "Security Policy\nParagraph B1."
    )
    chunks, metadatas = chunk_document(text, chunk_size=1000)
    assert chunks == [
        "Privacy Policy\n\nParagraph A1.",
        "Privacy Policy\n\nParagraph A2.",
        "Security Policy\n\nParagraph B1.",
    ]
    assert metadatas == [
        {"policy": "Privacy Policy"},
        {"policy": "Privacy Policy"},
        {"policy": "Security Policy"},
    ]
