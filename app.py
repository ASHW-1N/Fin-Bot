import streamlit as st
from rag_engine import get_nse_response

st.set_page_config(page_title="📈 StockSmartBot", layout="centered")
st.title("📈 NSE pro")
st.caption("Ask me about any Indian stock/index. I’ll give a SEBI-grade analysis.")

# Input area
query = st.text_input("📝 Enter your query (e.g., How did NIFTY50 perform today?)", "")

if query:
    with st.spinner("Analyzing market data..."):
        try:
            response = get_nse_response(query)
            st.markdown(response)
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
