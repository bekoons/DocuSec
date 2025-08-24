# 📄🔐 DocuSec

**DocuSec** is a lightweight, modular proof-of-concept trust center designed to automate compliance mapping and evidence extraction from policy and procedural documentation. It uses a Retrieval-Augmented Generation (RAG) pipeline to semantically analyze uploaded documents and map them to multiple security frameworks (e.g., ISO 27001, NIST 800-53, SOC 2).

---

## 🚧 Project Status

> **PoC in Progress**  
Designed for development in **GitHub Codespaces** using **Python 3.10+** and **Streamlit**.

---

## 🎯 Key Features

- ✅ Upload and parse security documentation (PDF, DOCX)
- ✅ Index content in a vector store via RAG
- ✅ Load and normalize multiple security frameworks
- ✅ Cross-reference controls between frameworks
- ✅ Query documents to extract compliance-relevant evidence

---

## 🧱 Project Structure

```
docusec/
├── app/
│   ├── main.py               # Streamlit app entrypoint
│   ├── ingestion.py          # Document parsing and chunking
│   ├── embeddings.py         # Embedding and vector store logic
│   ├── rag_pipeline.py       # RAG pipeline logic (retrieval + LLM reasoning)
│   ├── framework_loader.py   # Load ISO/NIST/SOC 2 control sets
│   ├── control_mapper.py     # Match documents to control frameworks
│   └── utils.py
├── database/
│   ├── schema.sql
│   └── seed_frameworks.json
├── vector_store/             # FAISS index files
├── .devcontainer/
│   └── devcontainer.json     # Codespaces configuration
├── requirements.txt
├── .env
└── README.md
```

---

## 💻 Getting Started in Codespaces

1. Open the repo in **GitHub Codespaces**
2. The environment will auto-install dependencies from `requirements.txt`
3. To run the app:

```bash
PYTHONPATH=$(pwd) streamlit run app/main.py
```

---

## ✅ Requirements

- Python 3.10+
- Streamlit
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
- Knowledge graph visualization
- Integration with GRC tools or Trust Center platforms
