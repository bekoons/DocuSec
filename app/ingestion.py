"""Utilities for ingesting policy documents."""

from typing import Callable, Dict, List, Tuple

from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import io

try:  # pragma: no cover - optional dependency
    from charset_normalizer import from_bytes
except Exception:  # pragma: no cover - library may be absent
    from_bytes = None

try:  # pragma: no cover - optional dependency
    import fitz  # type: ignore
except Exception:  # pragma: no cover - library may be absent
    fitz = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from docx import Document  # type: ignore
except Exception:  # pragma: no cover - library may be absent
    Document = None  # type: ignore


def read_file(
    data: bytes,
    filename: str | None = None,
    mime_type: str | None = None,
) -> str:
    """Decode raw file bytes into text using detected format.

    ``filename`` or ``mime_type`` may be supplied to hint at the file format.
    PDF documents are parsed with :mod:`PyMuPDF` and DOCX files via
    :mod:`python-docx`.  Plain text inputs fall back to charset detection using
    :mod:`charset_normalizer`.
    """

    filetype = None
    if mime_type:
        mt = mime_type.lower()
        if mt == "application/pdf":
            filetype = "pdf"
        elif mt == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            filetype = "docx"
        elif mt == "text/plain":
            filetype = "text"
    if filetype is None and filename:
        name = filename.lower()
        if name.endswith(".pdf"):
            filetype = "pdf"
        elif name.endswith(".docx"):
            filetype = "docx"
        elif name.endswith(".txt"):
            filetype = "text"

    if filetype == "pdf" and fitz is not None:  # pragma: no branch - depends on optional lib
        with fitz.open(stream=data, filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)

    if filetype == "docx" and Document is not None:  # pragma: no branch - depends on optional lib
        document = Document(io.BytesIO(data))
        return "\n".join(p.text for p in document.paragraphs)

    # Treat anything else as plain text
    if from_bytes is not None:
        try:
            result = from_bytes(data).best()
            if result is not None:
                return str(result)
        except Exception:
            pass
    return data.decode("utf-8", errors="ignore")


def _default_length_function(text: str) -> int:
    """Fallback length function counting characters when tokenizers are missing."""
    return len(text)


def chunk_document(
    text: str,
    chunk_size: int = 250,
    overlap: int = 50,
    length_func: Callable[[str], int] | None = None,
) -> Tuple[List[str], List[Dict[str, str]]]:
    """Split a policy document into chunks with policy-aware metadata.

    The first line of a policy is treated as the policy title.  Additional
    policies can be supplied in the same document by starting a new line that
    contains the word ``"policy"``.  Each policy body is further split into
    paragraphs, and long paragraphs are broken into token-aware subchunks.  A
    metadata dictionary is produced for every chunk indicating the policy it was
    derived from.

    Returns a tuple ``(chunks, metadatas)`` where ``chunks`` is a list of text
    snippets and ``metadatas`` contains a mapping with the originating policy
    title for each chunk.
    """

    if length_func is None:
        try:  # pragma: no cover - optional tokenizer dependency
            import tiktoken

            enc = tiktoken.get_encoding("cl100k_base")
            length_func = lambda txt: len(enc.encode(txt))
        except Exception:  # pragma: no cover - use simple fallback
            length_func = _default_length_function

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=length_func,
    )

    # Break the document into individual policy sections based on lines that
    # look like policy titles.
    policy_pattern = re.compile(r"policy", re.IGNORECASE)
    lines = text.splitlines()
    sections: List[Tuple[str, List[str]]] = []
    title: str | None = None
    buffer: List[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped and title is None:
            # Skip leading blank lines
            continue
        if title is None:
            # The first non-empty line is the initial policy title
            title = stripped
            continue

        if policy_pattern.search(stripped):
            # Encountered a new policy heading
            sections.append((title, buffer))
            title = stripped
            buffer = []
        else:
            buffer.append(stripped)

    if title is not None:
        sections.append((title, buffer))

    chunks: List[str] = []
    metadatas: List[Dict[str, str]] = []
    for policy_title, content_lines in sections:
        if not content_lines:
            chunks.append(policy_title)
            metadatas.append({"policy": policy_title})
            continue

        paragraph_text = "\n".join(content_lines)
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", paragraph_text) if p.strip()]
        for paragraph in paragraphs:
            for sub_chunk in splitter.split_text(paragraph):
                chunk = f"{policy_title}\n\n{sub_chunk}".strip()
                chunks.append(chunk)
                metadatas.append({"policy": policy_title})

    return chunks, metadatas

