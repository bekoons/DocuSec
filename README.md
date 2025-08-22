# 📄🔐 DocuSec

**DocuSec** is a lightweight, modular proof-of-concept trust center designed to automate compliance mapping and evidence extraction from policy and procedural documentation. By ingesting due diligence documents through a Retrieval-Augmented Generation (RAG) pipeline, DocuSec enables security and compliance teams to:

1. **Ingest** and semantically index documentation.
2. **Cross-map** security standards and frameworks (e.g., ISO 27001, NIST 800-53, SOC 2).
3. **Query** documents to demonstrate compliance with controls, including control-by-control evidence extraction.

---

## 🚧 Project Status

> **PoC in Progress**  
Architecture is structured as a modular monolith optimized for fast iteration and future scalability.

---

## 🎯 Key Features (PoC Goals)

- ✅ Upload and parse security documentation (PDF, DOCX)
- ✅ Index content in a vector store via RAG
- ✅ Load and normalize multiple security frameworks
- ✅ Cross-reference controls between frameworks
- ✅ Allow natural language queries like:  
  > *“Show me where this policy addresses ISO 27001 controls.”*
- ✅ Return tabular output mapping each control to relevant text excerpts

---

## 🧱 System Architecture (PoC)

```
docusec/
├── app/
│   ├── main.py               # FastAPI entrypoint
│   ├── ingestion.py          # Document parsing and chunking
│   ├── embeddings.py         # Embedding and vector store logic
│   ├── rag_pipeline.py       # RAG pipeline logic (retrieval + LLM reasoning)
│   ├── framework_loader.py   # Load ISO/NIST/SOC 2 control sets
│   ├── control_mapper.py     # Match documents to control frameworks
│   ├── ui.py                 # Streamlit or minimal React UI
│   └── utils.py
├── database/
│   ├── schema.sql
│   └── seed_frameworks.json  # Frameworks loaded as JSON/YAML
├── vector_store/             # FAISS index files
├── docker-compose.yml
├── Dockerfile
├── .env
└── README.md
```

---

## 📦 Tech Stack

| Layer        | Technology                  | Purpose                                  |
|--------------|------------------------------|------------------------------------------|
| Backend      | Python 3.10, FastAPI         | API layer for ingestion, RAG, and mapping |
| Frontend     | Streamlit *(or React)*       | Lightweight UI for document upload, query, and mapping views |
| NLP / RAG    | LangChain, OpenAI API        | Retrieval-augmented generation pipeline |
| Storage      | PostgreSQL                   | Stores metadata, document info, framework definitions |
| Vector Store | FAISS                        | Embedding similarity search |
| Container    | Docker + Docker Compose      | Dev/prod parity and deployment support |

---

## ✅ Requirements

- Python 3.10+
- Docker & Docker Compose
- OpenAI API key or compatible LLM
- Git

---

## 🚀 Milestones

### **Milestone 1: Core Setup**
- [ ] Create project structure and Docker setup
- [ ] Build FastAPI backend with health check
- [ ] Connect PostgreSQL and FAISS

### **Milestone 2: Document Ingestion + Embedding**
- [ ] Support DOCX/PDF file upload
- [ ] Extract text and chunk into RAG-ready format
- [ ] Embed and store in FAISS

### **Milestone 3: Framework Loading + Crosswalks**
- [ ] Load ISO 27001, NIST 800-53, SOC 2 controls
- [ ] Normalize control structure (ID, Title, Description)
- [ ] Implement basic crosswalk mapping logic

### **Milestone 4: RAG-Based Interrogation**
- [ ] Retrieve relevant chunks for each control
- [ ] Use LLM to map document content to each control
- [ ] Return results in tabular format

### **Milestone 5: Streamlit UI**
- [ ] Build simple UI to:
  - Upload files
  - Select framework
  - View control mappings and evidence excerpts
- [ ] Polish for demo/demo walkthrough

---

## 🔍 Example Query

> **"Show me how our InfoSec policy addresses ISO 27001."**

**Result:**

| ISO 27001 Control | Matching Excerpts from InfoSec Policy                              |
|------------------|---------------------------------------------------------------------|
| A.5.1.1          | • "The organization shall define an information security policy..." |
| A.9.2.1          | • "User access is reviewed every 90 days by the system owner."      |
| A.12.4.1         | • "Audit logs are maintained for administrative access..."          |

---

## 📌 Usage (Coming Soon)

```bash
# Clone the repo
git clone https://github.com/your-org/docusec.git
cd docusec

# Run the entire system
docker-compose up --build
```

---

## 🧭 Future Expansion Ideas

- Add control scoring confidence
- Export mappings as CSV or audit-ready PDF
- Admin role and version control for documents
- Knowledge graph visualization
- Integration with GRC tools or Trust Center platforms
