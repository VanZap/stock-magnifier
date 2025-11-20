from app import r
from events import notifier

class RedisManager:
    FAVORITES_KEY = "favorites"

    def __init__(self):
        pass
    
    # Saves stock quote data to Redis hash
    def save_stock(self, quote):
        if not quote:
            return None
        ticker = quote.get("01. symbol") or quote.get("symbol")
        if not ticker:
            return None

        data = {
            "ticker": ticker,
            "open": quote.get("02. open") or "",
            "high": quote.get("03. high") or "",
            "low": quote.get("04. low") or "",
            "price": quote.get("05. price") or "",
            "volume": quote.get("06. volume") or "",
            "latestTradingDay": quote.get("07. latest trading day") or "",
            "previousClose": quote.get("08. previous close") or "",
            "change": quote.get("09. change") or "",
            "changePercent": quote.get("10. change percent") or ""
        }
        redis_key = f"stock:{ticker}"
        try:
            r.hset(redis_key, mapping=data)
        except Exception as e:
            print("[ERROR] Redis save failed:", e)
            return None
        notifier.notify("stock_saved", {"ticker": ticker, "key": redis_key, "data": data})
        return redis_key

    # Adds ticker to favorites set
    def add_favorite(self, ticker):
        try:
            r.sadd(self.FAVORITES_KEY, ticker)
            notifier.notify("favorite_added", {"ticker": ticker})
        except Exception as e:
            print("[ERROR] Could not add favorite:", e)

    # Retrieves stock data from Redis
    def get_stock(self, ticker):
        redis_key = f"stock:{ticker}"
        try:
            if not r.exists(redis_key):
                return None
            return r.hgetall(redis_key)
        except Exception as e:
            print("[ERROR] Redis read failed:", e)
            return None
    
    # Get all favorited tickers, sorted alphabetically
    def list_favorites(self):
        try:
            members = r.smembers(self.FAVORITES_KEY) or set()
            return sorted(list(members))
        except Exception as e:
            print("[ERROR] Could not list favorites:", e)
            return []
    
    # Remove ticker from favorites
    def remove_favorite(self, ticker):
        try:
            removed = r.srem(self.FAVORITES_KEY, ticker)
            if removed:
                notifier.notify("favorite_removed", {"ticker": ticker})
            else:
                print(f"[Favorites] {ticker} not found on list.")
        except Exception as e:
            print("[ERROR] Could not remove favorite:", e)