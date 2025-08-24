from typing import Callable, List

from langchain.text_splitter import RecursiveCharacterTextSplitter


def read_file(data: bytes) -> str:
    """Decode raw file bytes into text."""
    return data.decode("utf-8", errors="ignore")


def _default_length_function(text: str) -> int:
    """Fallback length function counting characters when tokenizers are missing."""
    return len(text)


def chunk_document(
    text: str, chunk_size: int = 250, overlap: int = 50, length_func: Callable[[str], int] | None = None
) -> List[str]:
    """Split text into token-aware chunks."""
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
    return splitter.split_text(text)

