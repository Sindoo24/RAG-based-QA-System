import streamlit as st
import os

from ingestion import ingest_document
from chunking_embedding import chunk_document
from vectorstore import add_chunks_to_vectorstore
from query import retrieve_relevant_chunks
from llm import generate_answer
from config import UPLOAD_DIR, TOP_K



st.set_page_config(
    page_title="Multi-Modal RAG",
    layout="wide"
)

#  LOAD CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


#  SESSION STATE 
if "chats" not in st.session_state:
    st.session_state.chats = {}   # chat_id -> messages

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None



with st.sidebar:
    st.markdown("## 📂 Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        pdf_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Indexing document..."):
            doc_data = ingest_document(pdf_path)
            chunks = chunk_document(doc_data)
            add_chunks_to_vectorstore(chunks)

        chat_id = uploaded_file.name
        st.session_state.chats[chat_id] = []
        st.session_state.active_chat = chat_id

        st.success("Document indexed successfully")

    st.markdown("---")
    st.markdown("## 💬 Chats")

    for chat_id in st.session_state.chats:
        if st.button(chat_id, use_container_width=True):
            st.session_state.active_chat = chat_id


#  MAIN 
if not st.session_state.active_chat:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-orb"></div>
        <h1 class="hero-title">Hello, User</h1>
        <p class="hero-subtitle">How can I assist you today?</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


chat = st.session_state.chats[st.session_state.active_chat]



for msg in chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


#  USER INPUT 
user_input = st.chat_input("Ask anything about the document...")

if user_input:
    # User message
    chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Assistant response
    with st.spinner("Thinking..."):
        retrieved_chunks = retrieve_relevant_chunks(user_input, TOP_K)
        answer = generate_answer(user_input, retrieved_chunks)

    chat.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)

        with st.expander("📌 Sources"):
            for c in retrieved_chunks:
                st.write(
                    f"Page {c['metadata']['page']} ({c['metadata']['type']})"
                )

        #  SUMMARY 
        if st.button("✨ Summarize Answer"):
            with st.spinner("Summarizing..."):
                summary_prompt = (
                    "Summarize the following answer clearly and concisely:\n\n"
                    + answer
                )
                summary = generate_answer(summary_prompt, [])

            st.markdown("### 📝 Summary")
            st.write(summary)

