import os
import datetime as dt
import pandas as pd
from binance.client import Client

class CryptoDataFetcher:
    def __init__(self, debug=False):
        """Crypto veri çekme sınıfı."""
        self.api_key = os.getenv('API_KEY')
        self.secret_key = os.getenv('SECRET_KEY')
        self.client = Client(self.api_key, self.secret_key)
        self.debug = debug

    def debug_print(self, message):
        """Debug mesajlarını yazdırır."""
        if self.debug:
            print(f"[DEBUG] {message}")

    def fetch_and_save_data(self, symbols, timeframes, days=720):
        """Belirtilen semboller ve zaman aralıkları için veri çeker."""
        end_date = dt.datetime.now()

        for timeframe in timeframes:
            self.debug_print(f"Processing timeframe: {timeframe}")
            timeframe_dir = os.path.join('data', timeframe)
            os.makedirs(timeframe_dir, exist_ok=True)

            for symbol in symbols:
                self.debug_print(f"Fetching data for symbol: {symbol}")
                symbol_dir = os.path.join(timeframe_dir, symbol)
                os.makedirs(symbol_dir, exist_ok=True)

                interval = self.get_interval(timeframe)
                existing_file_path = os.path.join(symbol_dir, f"{symbol}_{timeframe}_data.csv")

                
                if os.path.exists(existing_file_path):
                    existing_df = pd.read_csv(existing_file_path)
                    self.debug_print(f"Existing data loaded: {len(existing_df)} rows")
                else:
                    existing_df = pd.DataFrame()
                    self.debug_print("No existing data found. Starting fresh.")

                
                klines = self.client.get_historical_klines(
                    symbol, interval,
                    start_str=(end_date - pd.DateOffset(days=days)).strftime("%d %b, %Y %H:%M:%S"),
                    end_str=end_date.strftime("%d %b, %Y %H:%M:%S"),
                )

                
                df = pd.DataFrame(klines, columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume', 
                    'close_time', 'quote_asset_volume', 'number_of_trades', 
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                ])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
                df['open'] = pd.to_numeric(df['open'])
                df['high'] = pd.to_numeric(df['high'])
                df['low'] = pd.to_numeric(df['low'])
                df['close'] = pd.to_numeric(df['close'])
                df['volume'] = pd.to_numeric(df['volume'])

                
                total_rows = len(df)
                self.debug_print(f"New data fetched: {total_rows} rows")
                for idx, row in enumerate(df.itertuples(), start=1):
                    if idx % 100 == 0:
                        self.debug_print(f"Processing row {idx}/{total_rows}")

                
                combined_df = pd.concat([existing_df, df]).drop_duplicates(subset='timestamp', keep='last')
                combined_df.sort_values('timestamp', inplace=True)

                
                new_data_count = len(combined_df) - len(existing_df)
                self.debug_print(f"New rows added: {new_data_count}")
                self.debug_print(f"Total data size: {len(combined_df)} rows")

                
                combined_df.to_csv(existing_file_path)
                print(f"{symbol} data for timeframe {timeframe} has been successfully updated in {existing_file_path}")

    @staticmethod
    def get_interval(timeframe):
        """Zaman aralığını Binance API için uygun formata dönüştürür."""
        intervals = {
            '1m': Client.KLINE_INTERVAL_1MINUTE,
            
        }
        return intervals.get(timeframe, Client.KLINE_INTERVAL_1DAY)


if __name__ == '__main__':
    fetcher = CryptoDataFetcher(debug=True)
    fetcher.fetch_and_save_data(
        symbols=['BTCUSDT'],
        timeframes=['1m'],
        days=720  
    )
