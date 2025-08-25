# 📄🔐 DocuSec

**DocuSec** is a portable, lightweight, modular proof-of-concept designed to automate compliance mapping and evidence extraction from policy and procedural documentation. It uses a Retrieval-Augmented Generation (RAG) pipeline to semantically analyze uploaded documents and map them to multiple security frameworks (e.g., ISO 27001, NIST 800-53, SOC 2).

After analyzing policy documents, control language is mapped to the relevant policy statements and displayed in a table showing potential control coverage evidence. 

---

## 🚧 Project Status

> **PoC in Progress**
Designed for development in **GitHub Codespaces** using **Python 3.10+**, **Streamlit**, and **FastAPI**.

---

## 🎯 Key Features

- ✅ Upload and parse policy documents (PDF, DOCX, TXT) with automatic encoding normalization
- ✅ Embed and persist policy content in FAISS vector stores
- ✅ Load and extend security frameworks stored in SQLite
- ✅ Build compliance control framework vector stores and check policy coverage
- ✅ Query documents via a Retrieval-Augmented Generation pipeline
- ✅ Access functionality through Streamlit and FastAPI interfaces

---

## 🧱 Project Structure

```
docusec/
├── app/
│   ├── api.py                # FastAPI endpoints
│   ├── main.py               # Streamlit app entrypoint
│   ├── ingestion.py          # Document parsing and chunking
│   ├── embeddings.py         # Embedding and vector store utilities
│   ├── rag_pipeline.py       # Retrieval + LLM reasoning
│   ├── framework_loader.py   # Load security control sets
│   ├── framework_vectors.py  # Build vector stores for frameworks
│   ├── control_mapper.py     # Match documents to controls
│   ├── db.py                 # SQLite helpers for frameworks
│   ├── ui.py                 # Minimal HTML snippets
│   └── utils.py              # Shared helpers
├── database/
│   ├── schema.sql
│   └── seed_frameworks.json
├── tests/                    # Unit tests
├── vector_store/             # Persisted FAISS indexes (created at runtime)
├── .devcontainer/
│   └── devcontainer.json     # Codespaces configuration
├── requirements.txt
└── README.md
```

---

## 💻 Getting Started in Codespaces

1. Clone the repo
2. Create secrets for the OpenAI API Key and Langchain API Key.
3. Open the repo in **GitHub Codespaces**
4. The environment will auto-install dependencies from `requirements.txt`
5. Run the Streamlit interface:

```bash
PYTHONPATH=$(pwd) streamlit run app/main.py
```

4. Or launch the FastAPI service:

```bash
PYTHONPATH=$(pwd) uvicorn app.api:app --reload
```

---

## ✅ Requirements

- Python 3.10+
- Streamlit
- FastAPI
- FAISS
- LangChain
- OpenAI API key (or compatible LLM provider)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔍 Example Query

> **"Show me how our InfoSec policy addresses ISO 27001."**

| ISO 27001 Control | Matching Excerpts from InfoSec Policy                              |
|------------------|---------------------------------------------------------------------|
| A.5.1.1          | • "The organization shall define an information security policy..." |
| A.9.2.1          | • "User access is reviewed every 90 days by the system owner."      |
| A.12.4.1         | • "Audit logs are maintained for administrative access..."          |

---

## 🧭 Future Expansion Ideas

- Add control scoring confidence
- Export mappings as CSV or audit-ready PDF
- Admin role and version control for documents
- Integration with GRC tools or Trust Center platforms