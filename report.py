import csv
import os
from models import Stock

# Handles report generation
class StockReportBuilder:
    def __init__(self):
        # for text report parts
        self.parts = []

        # for CSV rows
        self.rows = []
        # CSV header columns
        self.headers = ["ticker","price","open","high","low","volume",
                        "latestTradingDay","previousClose","change","changePercent"]

    # Clear previous build state
    def reset(self):
        self.parts.clear()
        self.rows.clear()
        return self

    # Text report
    def add_header(self, stock: Stock):
        self.parts.append(f"=== Stock Report: {stock.ticker} ===")
        return self

    def add_price_section(self, stock: Stock):
        self.parts.append(f"Price: {stock.price} | Open: {stock.open} | Prev Close: {stock.previousClose}")
        return self

    def add_volume_section(self, stock: Stock):
        self.parts.append(f"Volume: {stock.volume}")
        return self

    def add_change_section(self, stock: Stock):
        self.parts.append(f"Change: {stock.change} ({stock.changePercent})")
        return self

    def add_footer(self, stock: Stock):
        self.parts.append(f"Latest Trading Day: {stock.latestTradingDay}")
        self.parts.append("=" * 36)
        return self

    def build(self):
        return "\n".join(self.parts)

    # CSV report
    def add_row_for_csv(self, stock: Stock):
        self.rows.append([
            stock.ticker, stock.price or "", stock.open or "", stock.high or "",
            stock.low or "", stock.volume or "", stock.latestTradingDay or "",
            stock.previousClose or "", stock.change or "", stock.changePercent or ""
        ])
        return self

    def build_csv(self):
        return self.headers, self.rows
