from __future__ import annotations

import streamlit as st

from app.ingestion import parse_document
from app.embeddings import build_vector_store
from app.framework_loader import load_frameworks
from app.control_mapper import map_controls
from app.rag_pipeline import answer_query

st.set_page_config(page_title="DocuSec", page_icon="📄")

st.title("DocuSec Trust Center PoC")

# Initialize session state
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "store" not in st.session_state:
    st.session_state.store = None

st.header("1. Upload Documents")
uploaded_files = st.file_uploader(
    "Upload security documentation (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)

if uploaded_files:
    for file in uploaded_files:
        st.session_state.chunks.extend(parse_document(file))
    st.session_state.store = build_vector_store(st.session_state.chunks)
    st.success(f"Loaded {len(st.session_state.chunks)} text chunks.")

st.header("2. Framework Selection")
frameworks = load_frameworks()
selected_framework = st.selectbox("Select a control framework", frameworks)

if selected_framework and st.session_state.chunks:
    if st.button("Map Controls"):
        mappings = map_controls(st.session_state.chunks, selected_framework)
        st.subheader("Control Mappings")
        for mapping in mappings:
            st.markdown(f"**{mapping['control']}**: {mapping['excerpt']}")

st.header("3. Query Documents")
query = st.text_input("Ask a question about your documents")
if st.button("Run Query") and query:
    if st.session_state.store:
        response = answer_query(query, st.session_state.store)
        st.write(response)
    else:
        st.warning("Please upload documents first.")
