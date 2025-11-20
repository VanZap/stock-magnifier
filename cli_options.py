from models import AlphaVantageAdapter, Stock
from redis_manager import RedisManager
from report import StockReportBuilder
import os, csv

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
    
    def generate_report(self, report_folder="reports"):
        favorites = self.redis_mgr.list_favorites()
        if not favorites:
            print("No favorites to report.")
            return

        os.makedirs(report_folder, exist_ok=True)
        choice = input("Generate report as .csv or .txt format? (C/T, default C): ").strip().lower() or "c"
        is_csv = choice == "c"
        builder = StockReportBuilder().reset()

        for t in favorites:
            data = self.redis_mgr.get_stock(t)
            if not data:
                continue
            stock_obj = Stock(**data)
            if is_csv:
                builder.add_row_for_csv(stock_obj)
            else:
                builder.add_header(stock_obj).add_price_section(stock_obj).add_volume_section(stock_obj).add_change_section(stock_obj).add_footer(stock_obj)

        filename = os.path.join(report_folder, f"favorites_report.{ 'csv' if is_csv else 'txt' }")
        try:
            if is_csv:
                headers, rows = builder.build_csv()
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(rows)
            else:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(builder.build())
            print(f"[Report] Saved to {filename}")
        except Exception as e:
            print("[ERROR] Could not write report:", e)
