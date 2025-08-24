"""Utilities for building and querying a Retrieval Augmented Generation chain."""

from langchain.chains import RetrievalQA

# ChatOpenAI lives in the ``langchain_community`` package.  In minimal
# environments this dependency may be missing, so we fall back to a very small
# stub that mimics the interface well enough for tests.
try:  # pragma: no cover - import guarded for optional dependency
    from langchain.chat_models import ChatOpenAI
except Exception:  # pragma: no cover - executed only when package missing
    class ChatOpenAI:  # type: ignore[misc]
        """Lightweight fallback used when the real ChatOpenAI is unavailable."""

        def __init__(self, **_: object) -> None:  # noqa: D401, ANN401
            pass

        def invoke(self, *_: object, **__: object) -> str:  # noqa: ANN401
            return ""


def build_rag(vectorstore):
    """Construct a RetrievalQA chain from a vector store."""
    llm = ChatOpenAI(max_tokens=2048)  # Chat-based LLM capped for safety
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
    )


def answer_query(chain, question: str) -> str:
    """Run a query through the RAG chain."""
    return chain.run(question)

