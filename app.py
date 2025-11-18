import redis
import configparser

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
