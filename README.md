# 📈 StockSmartBot – Real-Time NSE Equity & Index Analyst

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

📈 StockSmartBot - Google Chrome 2025-07-03 16-25-17.gif

StockSmartBot is a real-time intelligent financial assistant that analyzes **live Indian stock market data** and returns expert-level reports — just like a SEBI-certified research analyst.

> Ask anything like:  
> _"How did Reliance perform today?"_  
> _"Give me today’s NIFTY 50 analysis."_  
> _"What’s happening with ABB India?"_  
> and get back **live**, detailed, professional-level financial analysis.

---

## 🚀 Features

- ✅ **Live Market Data (To-the-minute accuracy)**  
  Pulls real-time NSE data down to the **exact second you're asking**, unlike old models that wait for 3:30 PM to get data.

- 🤖 **LLM-powered Market Commentary**  
  Uses the **Groq LLaMA3-70B** model to write deep market analysis, technical commentary, and valuation insights.

- 🔍 **Smart Fuzzy Matching**  
  Automatically matches ticker symbols or company names (e.g., “ABB India”, “TCS”, “INFY”) even with typos or partial names.

- 📊 **Technical + Sentiment Analysis**  
  Uses:
  - Intraday price action
  - RSI, MACD, EMA trends
  - PE vs Sector PE
  - Volatility & investor behavior
  - Market sentiment insights

- 🧠 **Expert Prompt Engineering**  
  Prompts are tuned to mimic how seasoned SEBI analysts write their reports — natural, jargon-free, insightful.

- 🌐 **Plain English Queries Supported**  
  No need to type commands — just ask naturally like you would on Google.

---

## 🛠️ Tech Stack

| Component       | Tool / Library                             |
|-----------------|--------------------------------------------|
| 💬 LLM          | [Groq LLaMA3-70B](https://groq.com/)       |
| 📡 Data API     | [NseIndiaApi](https://github.com/BennyThadikaran/NseIndiaApi) |
| 🔎 Fuzzy Match   | [`rapidfuzz`](https://github.com/maxbachmann/RapidFuzz)      |
| 📊 Market Data  | `nselib` and `quote()` APIs for live data  |
| 🖥️ UI            | [`Streamlit`](https://streamlit.io)        |
| 🧪 Env Mgmt      | `python-dotenv` for managing secrets       |

---

## 💡 How It Works

1. You ask a natural query like _“How did ABB perform today?”_
2. Bot identifies whether you're asking about a **stock** or an **index**
3. It pulls **live data** from NSE at that very moment
4. A rich prompt is constructed using the data
5. It’s sent to **Groq's LLaMA3-70B** model
6. You get a full technical & valuation report written like a professional analyst

**Example Output**:
ABB India Limited closed 0.67% lower at ₹5866.5, indicating a bearish undertone...
[... full technical analysis follows ...]

🙏 Special Thanks
Special thanks to @BennyThadikaran for building NseIndiaApi, which powers the live data access for this project.

📌 Improvements Over Previous Version
✅ Now uses real-time data at the moment of query

✅ Much deeper, clearer, and well-written reports

✅ Better symbol and company matching (ABB, TCS, etc.)

✅ More stable API integration

✅ Professional-level prompt engineering for LLMs

