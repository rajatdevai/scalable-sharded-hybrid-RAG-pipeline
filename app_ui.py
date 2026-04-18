import streamlit as st
import requests
import os
import json
import time
from PyPDF2 import PdfReader
from app.config.constants import ALLOWED_CATEGORIES

# --- CONFIGURATION ---
API_URL = "http://localhost:8000"
st.set_page_config(page_title="Scalable Hybrid RAG", page_icon="🚀", layout="wide")

# --- STYLING ---
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .shard-tag {
        background-color: #1e2130;
        color: #00d4ff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- HELPERS ---
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ingest_data(docs):
    try:
        response = requests.post(f"{API_URL}/ingest", json={"documents": docs})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def query_rag(text):
    try:
        response = requests.post(f"{API_URL}/query", json={"query": text})
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- SIDEBAR (Monitoring & Ingestion) ---
with st.sidebar:
    st.title("⚙️ System Control")
    
    # Ingestion Tab
    with st.expander("📥 Data Ingestion", expanded=True):
        ingest_type = st.radio("Source", ["Text Paste", "File Upload"])
        
        if ingest_type == "Text Paste":
            raw_text = st.text_area("Paste content here...", height=200)
            if st.button("Ingest Text", use_container_width=True):
                if raw_text:
                    with st.spinner("Queueing..."):
                        res = ingest_data([raw_text])
                        st.success(res.get("message", "Queued!"))
                else:
                    st.warning("Please enter some text.")
                    
        else:
            files = st.file_uploader("Upload PDF or Text files", type=["pdf", "txt"], accept_multiple_files=True)
            if st.button("Ingest Files", use_container_width=True):
                if files:
                    with st.spinner("Processing files..."):
                        all_text = []
                        for f in files:
                            if f.name.endswith(".pdf"):
                                all_text.append(extract_pdf_text(f))
                            else:
                                all_text.append(f.read().decode("utf-8"))
                        res = ingest_data(all_text)
                        st.success(res.get("message", "Files queued!"))
                else:
                    st.warning("Please upload files first.")

    st.divider()
    
    # System Status
    st.subheader("📊 System Status")
    try:
        # Check health
        health = requests.get(f"{API_URL}/health").json()
        st.write("🟢 Server: Online")
    except:
        st.write("🔴 Server: Offline")
        
    st.write(f"**Categories:**")
    cols = st.columns(2)
    for i, cat in enumerate(ALLOWED_CATEGORIES):
        cols[i % 2].markdown(f"<span class='shard-tag'>{cat}</span>", unsafe_allow_html=True)

# --- MAIN CHAT INTERFACE ---
st.title("🚀 Scalable Hybrid RAG")
st.caption("AI-driven dynamic sharding with Cross-Encoder Re-ranking")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me anything about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_rag(prompt)
            
            if "answer" in response:
                answer = response["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # Optional: Show shard selection if we expose it in API
                # st.info("Intelligence: Intent matched to [Finance, HR]")
            else:
                error_msg = response.get("error", "Failed to get response")
                st.error(error_msg)
