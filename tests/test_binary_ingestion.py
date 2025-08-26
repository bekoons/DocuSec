import sys
from pathlib import Path
import io

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.ingestion import read_file


def test_read_file_pdf_docx(tmp_path):
    # create a simple PDF
    try:
        import fitz  # PyMuPDF
    except Exception:
        import pytest
        pytest.skip("PyMuPDF not available")
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello PDF")
    doc.save(pdf_path)
    data = pdf_path.read_bytes()
    assert "Hello PDF" in read_file(data, filename="sample.pdf")

    # create a simple DOCX
    try:
        from docx import Document
    except Exception:
        import pytest
        pytest.skip("python-docx not available")
    d = Document()
    d.add_paragraph("Hello DOCX")
    docx_path = tmp_path / "sample.docx"
    d.save(docx_path)
    data = docx_path.read_bytes()
    assert "Hello DOCX" in read_file(data, filename="sample.docx")
