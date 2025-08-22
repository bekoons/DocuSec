from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


def build_rag(vectorstore):
    """Construct a RetrievalQA chain from a vector store."""
    llm = OpenAI()
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


def answer_query(chain, question: str) -> str:
    """Run a query through the RAG chain."""
    return chain.run(question)

