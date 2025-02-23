import ccxt
import csv
from datetime import datetime, timedelta
import os

DATA_DIR = "trading_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

exchg = ccxt.binance() 
days_back = 50
symbol = 'BTC/USDT'
timeframe = '1m'

def fetch_binance_data(exchg, symbol, timeframe, days_back):
    since = exchg.parse8601((datetime.utcnow() - timedelta(days=days_back)).isoformat())
    try:
        data = exchg.fetchOHLCV(symbol, timeframe, since)
        if not data:
            print("No data retrieved")
        return data
    except Exception as e:
        print(f"Error fetching Binance data: {e}")
        return []

def save_to_csv(data, symbol, timeframe, filename):
    if not data:
        print("No data to save.")
        return
    
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            for row in data:
                writer.writerow(row)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"Error writing to file: {e}")

data = fetch_binance_data(exchg, symbol, timeframe, days_back)
save_to_csv(data, symbol, timeframe, 'binance.csv')