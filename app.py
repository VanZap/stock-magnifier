import redis
import configparser

class App:
    __instance = None

    def setup(self):
        config = configparser.ConfigParser()
        config.read("config.cfg")

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

def save_stock_to_redis(stock_data):
    """Save stock data (dict) to Redis Cloud."""
    ticker = stock_data.get("ticker")
    if not ticker:
        raise ValueError("stock_data must include a 'ticker' key")

    redis_key = f"stock:{ticker}"
    r.hset(redis_key, mapping=stock_data)
    print(f"Saved stock data for {ticker} to Redis under key '{redis_key}'.")

def get_stock_from_redis(ticker):
    """Retrieve stored stock data from Redis Cloud."""
    redis_key = f"stock:{ticker}"
    if not r.exists(redis_key):
        print(f"No data found in Redis for key '{redis_key}'.")
        return {}

    data = r.hgetall(redis_key)
    print(f"\nRetrieved data for {ticker} from Redis:")
    for k, v in data.items():
        print(f"  {k}: {v}")
    return data

if __name__ == "__main__":
    sample_stock = {
        "ticker": "DEMO",
        "open": "100.00",
        "high": "105.00",
        "low": "98.00",
        "price": "104.50",
        "volume": "150000",
        "latestTradingDay": "2025-10-24",
        "previousClose": "101.25",
        "change": "3.25",
        "changePercent": "3.21%"
    }

    save_stock_to_redis(sample_stock)
    get_stock_from_redis("DEMO")