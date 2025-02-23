import ccxt
print(ccxt.binance().fetchOHLCV('BTC/USDT', '1m'))