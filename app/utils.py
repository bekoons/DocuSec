from contextlib import contextmanager

try:  # pragma: no cover - optional dependency
    from langsmith.run_helpers import trace  # type: ignore[import]
except Exception:  # pragma: no cover - executed when langsmith missing
    @contextmanager
    def trace(_: str, **__: object):  # type: ignore[override]
        yield


def health() -> dict:
    """Simple health helper used by the API."""
    return {"status": "healthy"}

