import redis

r = redis.Redis(
    host='redis-13601.c276.us-east-1-2.ec2.redns.redis-cloud.com',
    port=13601,
    decode_responses=True,
    username="default",
    password="7U3INXqHnApSpEQUVe6p50Z8evJhuwKa",
)

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