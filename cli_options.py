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
    
    def display_favorites(self):
        favorites = self.redis_mgr.list_favorites()
        if not favorites:
            print("No favorites yet.")
            return

        print("\nSort favorites by:")
        print("  1) Ticker (alphabetical)")
        print("  2) Price (descending)")
        choice = input("Choose sort (1/2, default 1): ").strip() or "1"

        fav_with_data = [(t, self.redis_mgr.get_stock(t)) for t in favorites]
        if choice == "2":
            fav_with_data.sort(key=lambda x: float(x[1].get("price") or 0) if x[1] else 0, reverse=True)
        else:
            fav_with_data.sort(key=lambda x: x[0])

        print("\nFavorites:")
        for idx, (t, data) in enumerate(fav_with_data, start=1):
            price = data.get("price") if data else "N/A"
            print(f"{idx}. {t} | Price: {price}")

        delete = input("\nWould you like to delete a ticker from the list?\nEnter the number of ticker or press Enter to escape: ").strip()
        if delete.isdigit():
            i = int(delete) - 1
            if 0 <= i < len(fav_with_data):
                self.redis_mgr.remove_favorite(fav_with_data[i][0])
