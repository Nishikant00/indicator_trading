import pandas as pd
import pandas_ta as ta
import logging
from datetime import datetime
import os

DATA_DIR = "trading_data"
LOGS_DIR = "trading_logs"
for directory in [DATA_DIR, LOGS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  
    ]
)

class User:
    def __init__(self, user_id, rsi_overbought=70, rsi_oversold=30, indicators=None):
        self.user_id = user_id
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.indicators = indicators 

class TradeLogger:
    @staticmethod
    def get_log_file(indicator_name):
        return os.path.join(LOGS_DIR, f"{indicator_name.lower()}_trades.log")
    
    @staticmethod
    def log_trade(entry_time, entry_price, exit_time, exit_price,prev_rsi, rsi_entry, rsi_exit, indicator_name):
        profit_loss = ((exit_price - entry_price) / entry_price) * 100
        log_file = TradeLogger.get_log_file(indicator_name)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        
        logger = logging.getLogger(f"trade_logger_{indicator_name}")
        logger.setLevel(logging.INFO)
        
        logger.handlers = []
        logger.addHandler(file_handler)
        
        logger.info(
            f"Indicator: {indicator_name}, Entry Time: {entry_time}, Entry Price: ${entry_price:,.2f}, "
            f"Exit Time: {exit_time}, Exit Price: ${exit_price:,.2f}, "
            f"RSI Prev: {prev_rsi:.2f}, "
            f"RSI Entry: {rsi_entry:.2f}, RSI Exit: {rsi_exit:.2f}, "
            f"Profit/Loss: {profit_loss:.2f}%"
        )
        
        logger.removeHandler(file_handler)
        file_handler.close()

class TradingStrategy:
    def __init__(self, user: User, data: pd.DataFrame):
        self.user = user
        self.data = data
        self.logger = logging.getLogger("trading_strategy")
        self.apply_indicators()
        print(self.data)
    def apply_indicators(self):
        for indicator, params in self.user.indicators.items():
            if indicator == "RSI":
                self.data[indicator] = ta.rsi(self.data["close"], **params)
            elif indicator == "SMA":
                self.data[indicator] = ta.sma(self.data["close"], **params)
            elif indicator == "EMA":
                self.data[indicator] = ta.ema(self.data["close"], **params)

    def backtest(self):
        position = None
        entry_time, entry_price, rsi_entry = None, None, None
        indicator_name = "RSI"
        print(self.data)
        for i in range(1, len(self.data)):
            prev_rsi = self.data.iloc[i-1]["RSI"]
            curr_rsi = self.data.iloc[i]["RSI"]
            price = self.data.iloc[i]["close"]
            time = self.data.iloc[i]["timestamp"]
            print(time,prev_rsi, curr_rsi, price, time)
            if position is None:
                if prev_rsi <= self.user.rsi_oversold and curr_rsi > self.user.rsi_oversold:
                    position = "BUY"
                    entry_time, entry_price, rsi_entry = time, price, prev_rsi
                    self.logger.info(f"Time:{time} Opening LONG position using {indicator_name} - Price: ${price:,.2f},PREV_RSI: {prev_rsi:.2f}, RSI: {curr_rsi:.2f}")
            
            elif position == "BUY":
                if prev_rsi >= self.user.rsi_overbought and curr_rsi < self.user.rsi_overbought:
                    TradeLogger.log_trade(entry_time, entry_price, time, price,prev_rsi, rsi_entry, curr_rsi, indicator_name)
                    position = None

class BacktestEngine:
    def __init__(self, csv_file, user):
        self.logger = logging.getLogger("backtest_engine")
        csv_path = os.path.join(DATA_DIR, csv_file)
        if not os.path.exists(csv_path):
            self.logger.error(f"CSV file not found: {csv_path}")
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        self.data = pd.read_csv(csv_path)
        self.data["timestamp"] = pd.to_datetime(self.data["timestamp"], unit="ms")
        self.trading_strategy = TradingStrategy(user, self.data)

    def run(self):
        self.logger.info("Starting backtest...")
        self.trading_strategy.backtest()
        self.logger.info("Backtest completed")

if __name__ == "__main__":
    main_log_file = os.path.join(LOGS_DIR, "all_trades.log")
    file_handler = logging.FileHandler(main_log_file)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(file_handler)
    
    try:
        user = User(1, 70, 30, {"RSI": {"length": 14}, "SMA": {"length": 50}, "EMA": {"length": 20}})
        backtest = BacktestEngine("binance.csv", user)
        backtest.run()
    except Exception as e:
        logging.error(f"Error during backtest: {str(e)}", exc_info=True)