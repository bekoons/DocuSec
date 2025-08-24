import sys
import types
import asyncio
from pathlib import Path

# Stub minimal FastAPI interface for testing without external dependency
fastapi_stub = types.ModuleType("fastapi")


class UploadFile:
    def __init__(self, data: bytes):
        self._data = data

    async def read(self) -> bytes:  # noqa: D401
        return self._data


def File(*_args, **_kwargs):  # noqa: D401, ANN001
    return None


class FastAPI:
    def __init__(self, *args, **kwargs):  # noqa: D401, ANN401
        pass

    def get(self, *_args, **_kwargs):  # noqa: D401, ANN001
        def decorator(func):
            return func

        return decorator

    def post(self, *_args, **_kwargs):  # noqa: D401, ANN001
        def decorator(func):
            return func

        return decorator


fastapi_stub.FastAPI = FastAPI
fastapi_stub.UploadFile = UploadFile
fastapi_stub.File = File
responses_stub = types.ModuleType("fastapi.responses")
responses_stub.HTMLResponse = str
sys.modules["fastapi"] = fastapi_stub
sys.modules["fastapi.responses"] = responses_stub

# Make application code importable
sys.path.append(str(Path(__file__).resolve().parent.parent))

import app.api as api


def test_rag_query_returns_answer_within_token_limit(monkeypatch):
    class DummyChain:
        def run(self, question: str) -> str:  # noqa: D401
            return "short answer"

    def dummy_build_rag(_vectorstore):
        return DummyChain()

    def dummy_embed_and_store(_chunks):
        class _Store:
            def as_retriever(self, search_kwargs=None):  # noqa: D401, ANN001
                return self

        return _Store()

    monkeypatch.setattr(api, "embed_and_store", dummy_embed_and_store)
    monkeypatch.setattr(api, "build_rag", dummy_build_rag)
    monkeypatch.setattr(api, "answer_query", lambda chain, q: chain.run(q))

    async def run_flow():
        await api.ingest_document(UploadFile(b"hello world"))
        response = await api.query_rag("hi")
        return response

    data = asyncio.run(run_flow())
    assert data["answer"] == "short answer"
    assert len(data["answer"].split()) < 2048
