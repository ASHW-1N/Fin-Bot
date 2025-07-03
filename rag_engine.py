from nse import NSE
from pathlib import Path
from utils.index_matcher import fuzzy_index_match
from utils.equity_matcher import fuzzy_symbol_match
from groq_llm import generate_response_from_llm
import time

nse = NSE(download_folder=Path("."))

# --- Index data cache ---
try:
    indices_data = nse.listIndices()
    index_data_map = {
        entry["indexSymbol"].upper(): entry for entry in indices_data.get("data", [])
    }
except Exception as e:
    print(f"❌ Error fetching index data: {e}")
    index_data_map = {}

# --- Equity Prompt Formatter ---
def format_equity_prompt(entry: dict) -> str:
    info = entry.get("info", {})
    price = entry.get("priceInfo", {})
    meta = entry.get("metadata", {})
    security = entry.get("securityInfo", {})
    industry = entry.get("industryInfo", {})

    # Handle different API response structures
    last_price = price.get("lastPrice", price.get("last"))
    change = price.get("change", price.get("netPrice"))
    pct_change = price.get("pChange", price.get("netChange"))
    
    # Extract high/low data
    intraday_high_low = price.get("intraDayHighLow", {})
    if not intraday_high_low:
        intraday_high_low = {
            "min": price.get("low"),
            "max": price.get("high")
        }
    
    week_high_low = price.get("weekHighLow", {})
    if not week_high_low:
        week_high_low = {
            "min": price.get("low52"),
            "max": price.get("high52")
        }

    return f"""
You are a SEBI-registered equity research analyst with over 20 years of experience. Based on the following NSE data for {info.get('companyName', 'Unknown Company')} ({info.get('symbol', 'Unknown')}), write a deep analysis of today's market performance. Use advanced financial terms and include interpretations of price action, volatility, valuation, and investor sentiment.

Equity Snapshot:
- Symbol: {info.get("symbol", "N/A")}
- Company Name: {info.get("companyName", "N/A")}
- Industry: {industry.get("industry", info.get("industry", "N/A"))}
- Listing Date: {meta.get("listingDate", "N/A")}
- Last Price: {last_price}
- Change: {change} ({pct_change}%)
- Open: {price.get("open")}
- High: {intraday_high_low.get("max")}
- Low: {intraday_high_low.get("min")}
- Close: {price.get("close", price.get("lastPrice"))}
- Previous Close: {price.get("previousClose")}
- VWAP: {price.get("vwap")}
- 52W High: {week_high_low.get("max")}
- 52W Low: {week_high_low.get("min")}
- PE Ratio: {meta.get("pdSymbolPe", "N/A")}
- Sector PE: {meta.get("pdSectorPe", "N/A")}
- Sector: {meta.get("pdSectorInd", industry.get("sector", "N/A"))}
- Market Cap: {price.get("marketCap", "N/A")}
- Face Value: {security.get("faceValue", "N/A")}
- Volume: {price.get("totalTradedVolume", "N/A")}

Write the analysis in 150–300 words. Focus on insights and not just numbers. Avoid generic advice.
"""

# --- Index Prompt Formatter ---
def format_index_analysis_prompt(entry: dict) -> str:
    return f"""
You are a SEBI-registered senior market analyst with 20+ years of experience. Given the following raw NSE index data, write a professional, data-rich analysis for today.

Index Snapshot:
- Index Name: {entry.get('index')}
- Date: {entry.get('date365dAgo')}
- Open: {entry.get('open')}
- High: {entry.get('high')}
- Low: {entry.get('low')}
- Close: {entry.get('last')}
- Previous Close: {entry.get('previousClose')}
- Daily Change: {entry.get('variation')} ({entry.get('percentChange')}%)
- Year High/Low: {entry.get('yearHigh')} / {entry.get('yearLow')}
- 30d Change: {entry.get('perChange30d')}%
- 365d Change: {entry.get('perChange365d')}%
- PE Ratio: {entry.get('pe')}
- PB Ratio: {entry.get('pb')}
- Dividend Yield: {entry.get('dy')}
- Advances: {entry.get('advances')}
- Declines: {entry.get('declines')}
- Unchanged: {entry.get('unchanged')}

Write in natural, technical language. No generic suggestions.
"""

# --- Unified Entry Point ---
def get_nse_response(query: str) -> str:
    try:
        # First try index matching
        index_name = fuzzy_index_match(query)
        if index_name:
            entry = index_data_map.get(index_name.upper())
            if not entry:
                # Refresh index data if not found
                try:
                    indices_data = nse.listIndices()
                    index_data_map.update({
                        entry["indexSymbol"].upper(): entry for entry in indices_data.get("data", [])
                    })
                    entry = index_data_map.get(index_name.upper())
                except Exception:
                    pass
                
            if entry:
                prompt = format_index_analysis_prompt(entry)
                response = generate_response_from_llm(prompt)
                return f"📊 Detailed Market Analysis for {index_name}\n\n{response}"
            else:
                return f"⚠️ Index '{index_name}' not found. Try a different index name."

        # Then try equity matching
        symbol = fuzzy_symbol_match(query)
        if symbol:
            try:
                # First try without section
                equity_data = nse.quote(symbol, type="equity")
                
                # If priceInfo missing, try with trade_info
                if not equity_data.get("priceInfo"):
                    equity_data = nse.quote(symbol, type="equity", section="trade_info")
                
                # If still no price data, try alternative approach
                if not equity_data.get("priceInfo"):
                    # Try getting basic quote
                    basic_quote = nse.quote(symbol, type="equity", section="securityInfo")
                    if basic_quote:
                        equity_data.update(basic_quote)
                
                if equity_data.get("priceInfo") or equity_data.get("lastPrice"):
                    company_name = equity_data.get("info", {}).get("companyName", symbol)
                    prompt = format_equity_prompt(equity_data)
                    response = generate_response_from_llm(prompt)
                    return f"📈 Equity Analysis for {company_name} ({symbol})\n\n{response}"
                else:
                    return f"⚠️ NSE data incomplete for {symbol}. Please try another stock or try again later."
                
            except Exception as e:
                # Retry once after delay
                time.sleep(1)
                try:
                    equity_data = nse.quote(symbol, type="equity", section="trade_info")
                    if equity_data.get("priceInfo"):
                        company_name = equity_data.get("info", {}).get("companyName", symbol)
                        prompt = format_equity_prompt(equity_data)
                        response = generate_response_from_llm(prompt)
                        return f"📈 Equity Analysis for {company_name} ({symbol})\n\n{response}"
                except Exception as retry_error:
                    return f"⚠️ Error fetching data for {symbol}: {str(retry_error)}"
                
                return f"⚠️ Error processing {symbol}: {str(e)}"

        return "⚠️ Could not match your query to an index or equity. Try using full names like 'ABB India Limited' or symbols like 'ABB'"

    except Exception as e:
        return f"⚠️ System error: {str(e)}"