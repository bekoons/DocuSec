from __future__ import annotations

import requests
import streamlit as st

# Streamlit now communicates with a FastAPI backend instead of calling helper
# functions directly.  ``API_URL`` should point to the running backend
# instance.  In production, protect the API with authentication and transport
# security.
API_URL = "http://localhost:8000"

st.set_page_config(page_title="DocuSec", page_icon="📄")

st.title("DocuSec Trust Center PoC")

# Initialize session state
if "chunks" not in st.session_state:
    st.session_state.chunks = 0

st.header("1. Upload Documents")
uploaded_files = st.file_uploader(
    "Upload security documentation (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)

if uploaded_files:
    files = [("files", (file.name, file.getvalue())) for file in uploaded_files]
    resp = requests.post(f"{API_URL}/ingest", files=files, timeout=30)
    if resp.ok:
        st.session_state.chunks = resp.json().get("chunks", 0)
        st.success(f"Loaded {st.session_state.chunks} text chunks.")
    else:
        st.error("Document ingestion failed")

st.header("2. Framework Selection")
framework_resp = requests.get(f"{API_URL}/frameworks", timeout=30)
frameworks = framework_resp.json().get("frameworks", []) if framework_resp.ok else []
selected_framework = st.selectbox("Select a control framework", frameworks)

if selected_framework and st.session_state.chunks:
    if st.button("Map Controls"):
        map_resp = requests.post(
            f"{API_URL}/map_controls", json={"framework": selected_framework}, timeout=30
        )
        if map_resp.ok:
            mappings = map_resp.json()
            st.subheader("Control Mappings")
            for mapping in mappings:
                st.markdown(f"**{mapping['control']}**: {mapping['excerpt']}")
        else:
            st.error("Control mapping failed")

st.header("3. Query Documents")
query = st.text_input("Ask a question about your documents")
if st.button("Run Query") and query:
    query_resp = requests.post(f"{API_URL}/query", json={"query": query}, timeout=30)
    if query_resp.ok:
        st.write(query_resp.json().get("answer", ""))
    else:
        st.warning("Please upload documents first.")
