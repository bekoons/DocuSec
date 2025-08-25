import streamlit as st
import pandas as pd
from app.ingestion import read_file, chunk_document
from app.embeddings import (
    embed_and_store,
    save_vectorstore,
    list_vectorstores,
    load_vectorstore,
)

from app.rag_pipeline import build_rag, answer_query
from app.framework_loader import load_frameworks
from app.control_mapper import check_framework_coverage
from app.utils import ensure_utf8
from app.db import fetch_controls, store_csv_in_db
from app.validation import validate_input

# Streamlit frontend reusing core FastAPI logic
# This app leverages existing ingestion, RAG, and control mapping functions.

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# Initialize session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "frameworks" not in st.session_state:
    st.session_state.frameworks = load_frameworks()

st.title("DocuSec")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Ingest Policy Document",
        "Interrogate Policy",
        "Control Frameworks",
        "Framework Coverage",
    ],
)

if page == "Ingest Policy Document":
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    policy_name = st.text_input("Policy name")
    if uploaded_file is not None and policy_name and st.button("Ingest"):
        if uploaded_file.type not in ALLOWED_MIME_TYPES:
            st.error("Unsupported file type.")
        elif uploaded_file.size > MAX_FILE_SIZE:
            st.error("File too large. Limit 10MB.")
        else:
            text = read_file(uploaded_file.read())
            try:
                validate_input(text)
            except ValueError as err:
                st.error(str(err))
            else:
                chunks, metadatas = chunk_document(text)
                st.session_state.vectorstore = embed_and_store(chunks, metadatas)
                save_vectorstore(st.session_state.vectorstore, policy_name)
                st.session_state.rag_chain = build_rag(st.session_state.vectorstore)
                st.success(
                    f"Document ingested with {len(chunks)} chunks and saved as '{policy_name}'."
                )

elif page == "Interrogate Policy":
    st.header("Ask a Question")
    if st.session_state.rag_chain is None:
        st.info("Please ingest a document first.")
    else:
        question = st.text_input("Enter your question")
        if question:
            try:
                validate_input(question)
                answer = answer_query(st.session_state.rag_chain, question)
                st.write(answer)
            except ValueError as err:
                st.warning(str(err))
            except Exception as err:
                st.error(f"Failed to generate answer: {err}")

elif page == "Control Frameworks":
    st.header("Loaded Frameworks")
    st.json(fetch_controls())

    uploaded_csv = st.file_uploader(
        "Upload a framework CSV", type=["csv"]
    )
    if uploaded_csv is not None and st.button("Upload CSV"):
        if uploaded_csv.type != "text/csv":
            st.error("Unsupported file type.")
        elif uploaded_csv.size > MAX_FILE_SIZE:
            st.error("File too large. Limit 10MB.")
        else:
            try:
                count = store_csv_in_db(uploaded_csv.getvalue())
                st.success(f"Stored {count} controls.")
            except ValueError as err:
                st.warning(str(err))
            except Exception as err:
                st.error(f"Failed to process CSV: {err}")
        st.json(fetch_controls())

elif page == "Framework Coverage":
    st.header("Framework Coverage")
    controls = fetch_controls()
    frameworks = sorted({c["framework_title"] for c in controls})
    policies = list_vectorstores()
    if not frameworks:
        st.info("No frameworks available. Upload a framework CSV first.")
    elif not policies:
        st.info("No stored policies found. Ingest a policy first.")
    else:
        policy_choice = st.selectbox("Select a policy", policies)
        selected = st.selectbox("Select a framework", frameworks)
        if st.button("Check coverage"):
            vectorstore = load_vectorstore(policy_choice)
            selected_controls = [
                c for c in controls if c["framework_title"] == selected
            ]
            coverage = check_framework_coverage(vectorstore, selected_controls)
            if coverage:
                table_data = [
                    {
                        "Framework": c["framework_title"],
                        "Control Number": c["control_number"],
                        "Control Text": c["control_language"],
                        "Policy Excerpts": "\n\n".join(
                            ensure_utf8(e) for e in c["policy_excerpts"]
                        ),
                    }
                    for c in coverage
                ]
                st.table(pd.DataFrame(table_data))
            else:
                st.info("No controls found for selected framework.")
