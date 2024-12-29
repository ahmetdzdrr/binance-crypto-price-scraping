
# Crypto Data Fetcher

A Python application to fetch and store historical cryptocurrency data from Binance using its API. This script supports multiple symbols and multiple KLINE intervals (e.g., 1m, 5m, 15m, 30m, 1h, 4h, 1d).

---

## Table of Contents
- [Crypto Data Fetcher](#crypto-data-fetcher)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Supported KLINE Intervals](#supported-kline-intervals)
  - [Environment Variables](#environment-variables)
  - [Debug Mode](#debug-mode)

---

## Features
- Fetch historical KLINE (candlestick) data for multiple cryptocurrency symbols.
- Supports a wide range of intervals, including 1-minute (`1m`), 5-minute (`5m`), and daily (`1d`).
- Automatically merges and updates existing CSV files with new data.
- Saves data in a structured directory format for easy access.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/crypto-data-fetcher.git
   cd crypto-data-fetcher
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add your Binance API key and secret:
     ```env
     API_KEY=your_api_key
     SECRET_KEY=your_secret_key
     ```

---

## Usage

1. **Run the script**:
   ```bash
   python main.py
   ```

2. **Customize the fetcher**:
   - Modify the `symbols` list in the `main.py` script to include the cryptocurrencies you want to fetch (e.g., `['BTCUSDT', 'ETHUSDT']`).
   - Update the `timeframes` list to include the intervals you need (e.g., `['1m', '5m', '1h']`).
   - Adjust the `days` parameter to specify how far back in history you want the data (e.g., `days=365`).

---

## Supported KLINE Intervals

You can fetch data for the following Binance KLINE intervals:
- `1m` - 1 minute
- `5m` - 5 minutes
- `15m` - 15 minutes
- `30m` - 30 minutes
- `1h` - 1 hour
- `4h` - 4 hours
- `1d` - 1 day
- `1w` - 1 week
- `1M` - 1 month

To add more intervals, update the `get_interval` method in `main.py`:
```python
intervals = {
    '1m': Client.KLINE_INTERVAL_1MINUTE,
    '5m': Client.KLINE_INTERVAL_5MINUTE,
    '15m': Client.KLINE_INTERVAL_15MINUTE,
    '30m': Client.KLINE_INTERVAL_30MINUTE,
    '1h': Client.KLINE_INTERVAL_1HOUR,
    '4h': Client.KLINE_INTERVAL_4HOUR,
    '1d': Client.KLINE_INTERVAL_1DAY,
    '1w': Client.KLINE_INTERVAL_1WEEK,
    '1M': Client.KLINE_INTERVAL_1MONTH,
}
```

---

## Environment Variables

The script requires the following environment variables:
- **API_KEY**: Your Binance API key.
- **SECRET_KEY**: Your Binance secret key.

Set these in a `.env` file as shown in the [Installation](#installation) section.

---

## Debug Mode

To enable debug messages, set the `debug` parameter to `True` when initializing the `CryptoDataFetcher`:
```python
fetcher = CryptoDataFetcher(debug=True)
```

When enabled, the script will print detailed messages about its progress and any issues encountered.
