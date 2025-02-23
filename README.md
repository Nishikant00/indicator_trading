### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/Nishikant00/indicator_trading.git
    cd indicator_trading
    ```

2.  Create a virtual environment (recommended):

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Fetch Data:**

    ```bash
    python ccxt_binance_data_fetcher.py
    ```

    This script fetches historical data from Binance and saves it to the `trading_data/` directory.  You may need to configure API keys within this script.

2.  **Run Backtest:**

    ```bash
    python index.py
    ```

    This script runs the backtesting strategy using the data in `trading_data/` and saves trade logs to `trading_logs/`.
