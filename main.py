from app import API_KEY
from api import AlphaVantageFetcher, RateLimitProxy
from cli_options import CLIOptions

def main_loop():
    fetcher = AlphaVantageFetcher(API_KEY)
    proxy = RateLimitProxy(fetcher, min_interval=12.0)
    cli = CLIOptions(proxy)

    while True:
        print("\nSelect an option:")
        print("  1: Search Quote")
        print("  0: Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            cli.search_quote()
        elif choice == "0":
            print("Exited the app. Have a good day!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_loop()
