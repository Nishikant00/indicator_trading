import ccxt
import csv
from datetime import datetime, timedelta
import os

DATA_DIR = "trading_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

exchg = ccxt.binance() 
days_back = 5
symbol = 'BTC/USDT'
timeframe = '1m'

def fetch_binance_data(exchg, symbol, timeframe, days_back):
    since = exchg.parse8601((datetime.utcnow() - timedelta(days=days_back)).isoformat())
    all_data = []
    while True:
        try:
            data = exchg.fetchOHLCV(symbol, timeframe, since, limit=1000)
            if not data:
                print("No more data retrieved")
                break
            all_data.extend(data)
            since = data[-1][0] + 1  
        except Exception as e:
            print(f"Error fetching Binance data: {e}")
            break
    return all_data

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