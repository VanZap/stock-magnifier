import redis
import configparser
import requests

class App:
    __instance = None

    def setup(self):
        config = configparser.ConfigParser()
        config.read("config.cfg")

        # Setup Alpha Vantage Stocks API
        self.api_key = config["StocksAPI"]["apikey"].strip()

        # Setup Redis connection using config file
        self.dbconn = redis.Redis(
            host=config["Database"]["host"],
            port=int(config["Database"]["port"]),
            username=config["Database"]["username"],
            password=config["Database"]["password"],
            decode_responses=True
        )

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(App, cls).__new__(cls)
            cls.__instance.setup()
        return cls.__instance

app = App()
r = app.dbconn
API_KEY = app.api_key

# Fetch stock data from Alpha Vantage and print results
def fetch_stock_from_alpha_vantage(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url).json()
    quote = response.get("Global Quote", {})

    if not quote:
        print(f"No data found for symbol: {symbol}")
        return {}

    print(f"\nStock Data for {symbol}:")
    print(f"  Open: {quote.get('02. open')}")
    print(f"  High: {quote.get('03. high')}")
    print(f"  Low: {quote.get('04. low')}")
    print(f"  Price: {quote.get('05. price')}")
    print(f"  Volume: {quote.get('06. volume')}")
    print(f"  Latest Trading Day: {quote.get('07. latest trading day')}")
    print(f"  Previous Close: {quote.get('08. previous close')}")
    print(f"  Change: {quote.get('09. change')}")
    print(f"  Change Percent: {quote.get('10. change percent')}\n")

    return quote

# Fetch stock data from Alpha Vantage and save it to Redis Cloud
def save_stock_from_alpha_to_redis(symbol):
    quote = fetch_stock_from_alpha_vantage(symbol)
    if not quote:
        return

    data = {
        "ticker": quote.get("01. symbol"),
        "open": quote.get("02. open"),
        "high": quote.get("03. high"),
        "low": quote.get("04. low"),
        "price": quote.get("05. price"),
        "volume": quote.get("06. volume"),
        "latestTradingDay": quote.get("07. latest trading day"),
        "previousClose": quote.get("08. previous close"),
        "change": quote.get("09. change"),
        "changePercent": quote.get("10. change percent")
    }

    redis_key = f"stock:{data['ticker']}"
    r.hset(redis_key, mapping=data)
    print(f"Saved API stock data for {symbol} to Redis under key '{redis_key}'.")


def get_stock_from_redis_via_api(symbol):
    """Retrieve the stock data previously saved to Redis Cloud."""
    redis_key = f"stock:{symbol}"
    if not r.exists(redis_key):
        print(f"No data found in Redis for key '{redis_key}'.")
        return {}

    data = r.hgetall(redis_key)
    print(f"\nRetrieved {symbol} data from Redis:")
    for k, v in data.items():
        print(f"  {k}: {v}")
    return data


if __name__ == "__main__":
    symbol = "TSLA"

    save_stock_from_alpha_to_redis(symbol)
    get_stock_from_redis_via_api(symbol)