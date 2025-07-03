from pathlib import Path
from nse import NSE
from nselib import capital_market
from rapidfuzz import fuzz, process

nse = NSE(download_folder=Path("."))

# Load equity list ONCE
try:
    equity_list_data = capital_market.equity_list()
    SYMBOLS = {entry.get("SYMBOL"): entry.get("NAME OF COMPANY", "") for entry in equity_list_data if entry.get("SYMBOL")}
except Exception as e:
    SYMBOLS = {}
    print(f"❌ Failed to load NSE equity list: {e}")

def fuzzy_symbol_match(query: str) -> str | None:
    """
    Enhanced matching algorithm using:
    1. Exact symbol matches
    2. Company name matches
    3. Fuzzy matching with rapidfuzz
    4. API fallback
    """
    query = query.upper().replace("?", "").replace(",", "").strip()
    words = query.split()
    
    # 1. Try exact symbol match in loaded symbols
    for word in words:
        if word in SYMBOLS:
            return word
            
    # 2. Try company name match
    for symbol, company in SYMBOLS.items():
        if company.upper() in query:
            return symbol
            
    # 3. Fuzzy matching with rapidfuzz
    # Match against symbols
    symbol_match = process.extractOne(query, SYMBOLS.keys(), scorer=fuzz.WRatio, score_cutoff=80)
    # Match against company names
    company_match = process.extractOne(query, SYMBOLS.values(), scorer=fuzz.WRatio, score_cutoff=80)
    
    if symbol_match and symbol_match[1] > 85:
        return symbol_match[0]
    if company_match and company_match[1] > 85:
        # Find symbol for matched company name
        return next((s for s, c in SYMBOLS.items() if c == company_match[0]), None)
    
    # 4. Fallback to NSE API
    for word in words:
        try:
            response = nse.quote(symbol=word, type="equity")
            if response and "info" in response and response["info"].get("symbol") == word:
                return word
        except Exception:
            continue
            
    # 5. Final fuzzy attempt with lower threshold
    if symbol_match and symbol_match[1] > 70:
        return symbol_match[0]
    if company_match and company_match[1] > 70:
        return next((s for s, c in SYMBOLS.items() if c == company_match[0]), None)
    
    return None
