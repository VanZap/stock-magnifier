class Stock:
    # Normalized stock object
    def __init__(self, ticker, open=None, high=None, low=None, price=None,
                 volume=None, latestTradingDay=None, previousClose=None, change=None, changePercent=None):
        self.ticker = ticker
        self.open = open
        self.high = high
        self.low = low
        self.price = price
        self.volume = volume
        self.latestTradingDay = latestTradingDay
        self.previousClose = previousClose
        self.change = change
        self.changePercent = changePercent

    def to_dict_for_redis(self):
        return {
            "ticker": self.ticker,
            "open": self.open or "",
            "high": self.high or "",
            "low": self.low or "",
            "price": self.price or "",
            "volume": self.volume or "",
            "latestTradingDay": self.latestTradingDay or "",
            "previousClose": self.previousClose or "",
            "change": self.change or "",
            "changePercent": self.changePercent or ""
        }

    def clone(self):
        return Stock(**self.__dict__)

# Converts API quote dictionary to Stock object.
class AlphaVantageAdapter:
    @staticmethod
    def from_api(quote):
        if not quote:
            return None

        def g(k): return quote.get(k) or quote.get(k.replace(".", "")) or quote.get(k.lower()) or None
        ticker = g("01. symbol") or g("symbol")

        return Stock(
            ticker=ticker,
            open=g("02. open"),
            high=g("03. high"),
            low=g("04. low"),
            price=g("05. price"),
            volume=g("06. volume"),
            latestTradingDay=g("07. latest trading day"),
            previousClose=g("08. previous close"),
            change=g("09. change"),
            changePercent=g("10. change percent")
        )
