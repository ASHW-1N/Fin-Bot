def fuzzy_index_match(query: str) -> str:
    mapping = {
        "nifty50": "NIFTY 50",
        "banknifty": "NIFTY BANK",
        "niftybank": "NIFTY BANK",
        "niftynext50": "NIFTY NEXT 50",
        "finnifty": "FINNIFTY",
        "midcap": "NIFTY MIDCAP 50",
        "niftymidcap50": "NIFTY MIDCAP 50",
    }
    query = query.lower().replace(" ", "")
    for key in mapping:
        if key in query:
            return mapping[key]
    return None
