import os
import sys
import types
import asyncio
from pathlib import Path

# Stub minimal FastAPI interface for testing without external dependency
fastapi_stub = types.ModuleType("fastapi")


class UploadFile:
    def __init__(self, data: bytes, content_type: str = "text/plain"):
        self._data = data
        self.content_type = content_type

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

    def add_middleware(self, *args, **kwargs):  # noqa: D401, ANN001
        pass

    def post(self, *_args, **_kwargs):  # noqa: D401, ANN001
        def decorator(func):
            return func

        return decorator


fastapi_stub.FastAPI = FastAPI
fastapi_stub.UploadFile = UploadFile
fastapi_stub.File = File

def Depends(dependency):  # noqa: D401, ANN001
    return dependency


class HTTPException(Exception):  # noqa: D401
    def __init__(self, status_code: int, detail: str):  # noqa: D401, ANN401
        self.status_code = status_code
        self.detail = detail


status_stub = types.ModuleType("status")
status_stub.HTTP_401_UNAUTHORIZED = 401


security_stub = types.ModuleType("fastapi.security")


class APIKeyHeader:  # noqa: D401
    def __init__(self, name: str, auto_error: bool = True):  # noqa: D401, ANN401
        self.name = name
        self.auto_error = auto_error

    async def __call__(self):  # noqa: D401
        return "test"


security_stub.APIKeyHeader = APIKeyHeader

sys.modules["fastapi.security"] = security_stub

fastapi_stub.Depends = Depends
fastapi_stub.HTTPException = HTTPException
fastapi_stub.status = status_stub
sys.modules["fastapi.status"] = status_stub

responses_stub = types.ModuleType("fastapi.responses")
responses_stub.HTMLResponse = str
sys.modules["fastapi"] = fastapi_stub
sys.modules["fastapi.responses"] = responses_stub

# Make application code importable
sys.path.append(str(Path(__file__).resolve().parent.parent))
# Configure expected secret for API authentication
os.environ.setdefault("LANGCHAIN_API_KEY", "test")

import app.api as api


def test_rag_query_returns_answer_within_token_limit(monkeypatch):
    class DummyChain:
        def run(self, question: str) -> str:  # noqa: D401
            return "short answer"

    def dummy_build_rag(_vectorstore):
        return DummyChain()

    def dummy_embed_and_store(_chunks, _metadatas=None):
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
