import os
from nselib import capital_market
import pandas as pd

# GROQ (LLM) API access
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama3-8b-8192"

def extract_symbol_from_query(query: str) -> str:
    query = query.lower()
    mapping = {
        "reliance": "RELIANCE",
        "tcs": "TCS",
        "infosys": "INFY",
        "hdfc": "HDFC",
        "icici": "ICICIBANK",
        "nifty": "NIFTY",
        "sensex": "SENSEX"
    }
    for key, symbol in mapping.items():
        if key in query:
            return symbol
    return ""

def analyze_market_data(user_query: str) -> str:
    try:
        symbol = extract_symbol_from_query(user_query)
        if not symbol:
            return "⚠️ Sorry, I couldn't determine the stock symbol from your question."

        df = capital_market.price_volume_and_deliverable_position_data(symbol=symbol, period='1D')

        if df.empty or len(df) == 0:
            return f"❌ No market data available for {symbol.upper()} today."

        # DEBUG: Print actual column names to ensure correct mapping
        print("Original columns:", df.columns.tolist())

        # Hardcode correct mapping from NSE-delivered columns
        expected_columns = [
            "Symbol", "Series", "Date", "Prev Close", "Open Price", "High Price", "Low Price",
            "Last Price", "Close Price", "Average Price", "Total Traded Quantity",
            "Turnover In Rs", "No. of Trades", "Deliverable Qty", "% Dly Qt to Traded Qty"
        ]
        df.columns = [col.strip() for col in expected_columns]

        latest = df.iloc[-1]

        def to_float(val):
            try:
                return float(str(val).replace(",", "").strip())
            except:
                return 0.0

        def to_int(val):
            try:
                return int(float(str(val).replace(",", "").strip()))
            except:
                return 0

        open_price = to_float(latest["Open Price"])
        close_price = to_float(latest["Close Price"])
        high = to_float(latest["High Price"])
        low = to_float(latest["Low Price"])
        volume = to_int(latest["Total Traded Quantity"])
        date = latest["Date"]

        if open_price == 0 and close_price == 0:
            return f"⚠️ Market data for {symbol.upper()} today appears to be missing or incomplete."

        return (
            f"📈 {symbol.upper()} on {date}:\n"
            f"Opened at ₹{open_price:.2f}, closed at ₹{close_price:.2f}.\n"
            f"Day's range: ₹{low:.2f} - ₹{high:.2f}.\n"
            f"Total traded volume: {volume:,} shares."
        )

    except Exception as e:
        return f"❌ Error fetching stock data: {str(e)}"

def run_rag_pipeline(user_query: str) -> str:
    """
    Combines stock data and LLM if needed (currently only stock query path).
    """
    if any(keyword in user_query.lower() for keyword in ["perform", "today", "price", "volume", "how did", "close"]):
        return analyze_market_data(user_query)

    # fallback LLM answer
    return ask_llm(user_query)

def ask_llm(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ LLM Error: {str(e)}"
