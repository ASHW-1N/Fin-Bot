# app.py
import streamlit as st
from rag_engine import run_rag_pipeline

st.set_page_config(page_title="Financial RAG Assistant", layout="centered")
st.title("📊 Financial RAG Chatbot")

query = st.text_input("Ask about any stock (e.g., How did Reliance perform today?)")

if st.button("Get Answer") and query:
    with st.spinner("Fetching data..."):
        response = run_rag_pipeline(query)
        st.markdown("### 💬 Answer")
        st.write(response)
