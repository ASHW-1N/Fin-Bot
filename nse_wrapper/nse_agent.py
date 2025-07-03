from nse import NSE
from nselib import capital_market

class NseAgent:
    def __init__(self):
        # Initialize NSE instance with local mode (not server)
        self.nse = NSE(download_folder="")

        # Load all equity symbols from nselib (used only for equity list)
        equity_list_data = capital_market.equity_list()
        self.equity_symbols = [entry.get("SYMBOL") for entry in equity_list_data if entry.get("SYMBOL")]

        # Load index names safely from NSE rich data
        index_data = self.nse.listIndices()
        self.index_list = []
        for entry in index_data.get("data", []):
            if "index" in entry:
                self.index_list.append(entry["index"])
            elif "name" in entry:
                self.index_list.append(entry["name"])

        # Map available functions
        self.function_map = {
            "equity_quote": self.nse.equityQuote,
            "quote": self.nse.quote,
            "index_data": self.nse.indexData,               
            "equity_list": capital_market.equity_list      
        }

    def get_equity_symbols(self):
        return self.equity_symbols

    def get_index_names(self):
        return self.index_list

    def get_function_map(self):
        return self.function_map

    def close(self):
        self.nse.exit()
