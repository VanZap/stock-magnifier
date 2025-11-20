import requests
import time

# Simple wrapper for the Alpha Vantage API
class AlphaVantageFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    # Fetch stock data for a given symbol from Alpha Vantage.
    def fetch(self, symbol):
        url = (
            f"https://www.alphavantage.co/query?"
            f"function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}"
        )
        try:
            response = requests.get(url, timeout=10).json()
        except Exception as e:
            print("[ERROR] API request failed:", e)
            return {}

        quote = response.get("Global Quote", {})
        if not quote:
            print(f"No data found for symbol: {symbol}")
            return {}

        print(f"\nStock Data for {symbol}:")
        for k, v in quote.items():
            print(f"  {k}: {v}")
        print()
        return quote

# Proxy enforcing rate limit and caching API responses
class RateLimitProxy:
    def __init__(self, real_fetcher, min_interval=12.0):
        self._real = real_fetcher
        # add minimum delay between requests
        self._min_interval = float(min_interval)
        # track last request time for rate limiting
        self._last_call = 0.0
        # cache results to avoid repeated API calls
        self._cache = {}

    # Fetch with caching and enforced delay.
    def fetch(self, symbol):
        if symbol in self._cache:
            return self._cache[symbol]

        now = time.time()
        elapsed = now - self._last_call
        # enforce minimum interval between API calls
        if elapsed < self._min_interval:
            wait_for = self._min_interval - elapsed
            print(f"[Proxy] Waiting {wait_for:.1f}s due to rate limit...")
            time.sleep(wait_for)
        self._last_call = time.time()

        result = self._real.fetch(symbol)
        if result:
            self._cache[symbol] = result
        return result
