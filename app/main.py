import streamlit as st
from ingestion import read_file, chunk_document
from embeddings import embed_and_store
from rag_pipeline import build_rag, answer_query
from framework_loader import load_frameworks
from control_mapper import map_controls as perform_control_mapping

# Streamlit frontend reusing core FastAPI logic
# This app leverages existing ingestion, RAG, and control mapping functions.

# Initialize session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "frameworks" not in st.session_state:
    st.session_state.frameworks = load_frameworks()

st.title("DocuSec")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Ingest Policy Document", "Interrogate Policy", "Control Frameworks", "Map Controls"])

if page == "Ingest Policy Document":
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        text = read_file(uploaded_file.read())
        chunks = chunk_document(text)
        st.session_state.vectorstore = embed_and_store(chunks)
        st.session_state.rag_chain = build_rag(st.session_state.vectorstore)
        st.success(f"Document ingested with {len(chunks)} chunks.")

elif page == "Interrogate Policy":
    st.header("Ask a Question")
    if st.session_state.rag_chain is None:
        st.info("Please ingest a document first.")
    else:
        question = st.text_input("Enter your question")
        if question:
            answer = answer_query(st.session_state.rag_chain, question)
            st.write(answer)

elif page == "Control Frameworks":
    st.header("Loaded Frameworks")
    st.json(st.session_state.frameworks)

elif page == "Map Controls":
    st.header("Map Text to Framework Controls")
    text_input = st.text_area("Enter text to map to controls")
    if st.button("Map Controls"):
        if text_input:
            mapping = perform_control_mapping(st.session_state.frameworks, [text_input])
            st.json(mapping)
        else:
            st.warning("Please provide text to map.")
