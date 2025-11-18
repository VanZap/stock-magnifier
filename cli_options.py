from models import AlphaVantageAdapter
from redis_manager import RedisManager

# Handles user interaction and CLI options
class CLIOptions:
    def __init__(self, proxy_fetcher):
        self.proxy_fetcher = proxy_fetcher
        self.redis_mgr = RedisManager()

    def search_quote(self):
        symbol = input("Enter ticker symbol (e.g., TSLA): ").strip().upper()
        if not symbol:
            print("No symbol entered.")
            return
        raw = self.proxy_fetcher.fetch(symbol)
        if not raw:
            print("No quote returned.")
            return
        self.redis_mgr.save_stock(raw)
        stock_obj = AlphaVantageAdapter.from_api(raw)
        if input("Add to favorites? (y/N): ").strip().lower() == "y":
            self.redis_mgr.add_favorite(stock_obj.ticker)
