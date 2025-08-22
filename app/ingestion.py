from __future__ import annotations

from io import BytesIO
from typing import List

import fitz  # PyMuPDF
from docx import Document

from .utils import chunk_text


def parse_document(uploaded_file) -> List[str]:
    """Parse an uploaded PDF or DOCX file into text chunks.

    The file contents are read into memory, converted to plain text and then
    split using :func:`chunk_text`.

    Security considerations
    -----------------------
    * Uploaded files are treated as untrusted input.  Only ``pdf`` and ``docx``
      extensions are processed to reduce risk from malicious formats.
    * No malware scanning or content validation is performed.  In production,
      run server-side antivirus and consider file size limits to avoid
      resource-exhaustion attacks.
    * Parsed text is held in memory; consider user authentication and access
      controls before exposing extracted data.
    """
    data = uploaded_file.read()
    name = uploaded_file.name.lower()

    text = ""
    if name.endswith(".pdf"):
        doc = fitz.open(stream=data, filetype="pdf")
        for page in doc:
            text += page.get_text()
    elif name.endswith(".docx"):
        doc = Document(BytesIO(data))
        text = "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type: %s" % uploaded_file.name)

    return chunk_text(text)
