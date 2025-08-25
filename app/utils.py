from contextlib import contextmanager
from typing import Any

try:  # pragma: no cover - optional dependency
    from langsmith.run_helpers import trace  # type: ignore[import]
except Exception:  # pragma: no cover - executed when langsmith missing
    @contextmanager
    def trace(_: str, **__: object):  # type: ignore[override]
        yield


def health() -> dict:
    """Simple health helper used by the API."""
    return {"status": "healthy"}


try:  # pragma: no cover - optional dependency
    from charset_normalizer import from_bytes as _from_bytes
except Exception:  # pragma: no cover - executed when library missing
    _from_bytes = None


def ensure_utf8(text: Any) -> str:
    """Return ``text`` as a UTF-8 encoded string.

    ``text`` may be raw bytes from a vector store or any object that can be
    stringified. Bytes are decoded using :mod:`charset_normalizer` when
    available, falling back to UTF-8 with ``errors="ignore"``. Non-string
    objects are coerced to strings and re-encoded as UTF-8 to strip any invalid
    characters.
    """

    if isinstance(text, bytes):
        if _from_bytes is not None:
            try:
                result = _from_bytes(text).best()
                if result is not None:
                    return str(result)
            except Exception:
                pass
        return text.decode("utf-8", errors="ignore")

    if not isinstance(text, str):
        text = str(text)
    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

