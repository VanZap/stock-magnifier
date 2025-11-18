from app import r
from events import Notifier

class RedisManager:
    FAVORITES_KEY = "favorites"

    def __init__(self):
        self.notifier = Notifier()

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
        return redis_key

    def add_favorite(self, ticker):
        try:
            r.sadd(self.FAVORITES_KEY, ticker)
            print(f"Successfuly added {ticker} to favorites!")
        except Exception as e:
            print("[ERROR] Could not add favorite:", e)