# Stock Magnifier App

The **Stock Magnifier App** is a lightweight, modular tool for fetching, storing, and generating stock market data report. It integrates with the **AlphaVantage API** to retrieve real-time and historical stock quotes and persists the processed data in **Redis Cloud**. A clean command-line interface (CLI) enables quick access to all core functionality.

---

## Features

- **Real-time Stock Data**: Fetch current stock quotes from AlphaVantage API
- **Persistent Storage**: Store and manage stock data in Redis Cloud
- **Favorites Management**: Add, remove, and organize your favorite tickers
- **Smart Sorting**: View favorites alphabetically or by price (descending)
- **Report Generation**: Export favorites as CSV or formatted text reports
- **Rate Limiting**: Built-in proxy to handle API rate limits

---

## Project Structure

```
project/
|
|-- config.cfg          # Configuration file (API keys, Redis URLs, etc.)
|-- app.py              # App initialization, DB and API setup (Singleton)
|-- models.py           # Stock data model
|-- api.py              # Alpha Vantage API fetching operations
|-- redis_manager.py    # Encapsulated Redis operations
|-- cli_options.py      # CLI interface definitions
|-- main.py             # Application entry point
|-- report.py           # Report generation (csv / txt format)
|-- events.py           # Observer for events
```

---

## Architecture Overview

This project follows several software design patterns to ensure maintainability and clean abstraction layers.

| Pattern       | Component             | Description                                               |
| ------------- | --------------------- | --------------------------------------------------------- |
| **Singleton** | `app.py`              | Ensures only one instance is used for DB and API setup.   |
| **Adapter**   | `AlphaVantageAdapter` | Converts raw API responses into internal `Stock` objects. |
| **Proxy**     | `RateLimitProxy`      | Adds rate limiting and caching to AlphaVantage API calls. |
| **Builder**   | `StockReportBuilder`  | Generates report in csv/ txt format                       |
| **Observer**   | `Notifier`           | Notifies system of important events                       |
---

## How It Works

### 1. AlphaVantage API Fetching

`api.py` handles HTTP requests and delegates response transformation to the **Adapter**, ensuring consistent `Stock` model formatting.

### 2. Redis Cloud Storage

`redis_manager.py` abstracts all Redis interactions, including storing, fetching, and updating stock entries.

### 3. Application Setup

`app.py` acts as a **Singleton**, initializing:

* API client
* Redis connection
* Core services

### 4. CLI Interface

Using `cli_options.py`, users can:

* Fetch a stock
* Add to favorites
* Display favorites
* Sort favorites
* Delete ticker
* Generate report

All CLI commands route through `main.py`.

---

## Usage

### 1. Prerequisites

- AlphaVantage API key
- Redis instance

### Setup

#### 2. Configure Credentials

Create or edit `config.cfg` with your credentials:

```ini
[StocksAPI]
apikey = YOUR_ALPHAVANTAGE_API_KEY

[Database]
host = your-redis-host.redis.com
port = 6379
username = default
password = your-redis-password
```

#### 3. Run the Application

```bash
python main.py
```

