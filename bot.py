import alpaca_trade_api as tradeapi
import pandas as pd
import schedule
import time
from config import API_KEY, SECRET_KEY, BASE_URL

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# Define a function to fetch historical data
def fetch_data(symbol, timeframe, limit=100):
    bars = api.get_bars(symbol, timeframe, limit=limit).df
    return bars

# Define a basic strategy: Buy if price is under $150
def simple_strategy():
    symbol = "AAPL"  # Replace with your stock symbol
    bars = fetch_data(symbol, "minute", limit=1)
    price = bars[-1].close  # Last closing price

    print(f"{symbol} price: {price}")
    try:
        if float(price) < 150:
            # Place a buy order
            api.submit_order(
                symbol=symbol,
                qty=1,
                side="buy",
                type="market",
                time_in_force="gtc"
            )
            print(f"Bought 1 share of {symbol}!")
    except ValueError:
        print("Invalid price value")

iterations = 0
max_iterations = 10  # Set the maximum number of iterations

# Schedule the bot to run every minute
schedule.every(1).minute.do(simple_strategy)

while iterations < max_iterations:
    try:
        schedule.run_pending()
        time.sleep(1)
        iterations += 1
    except Exception as e:
        print(f"An error occurred: {e}")
        break

while True:
    simple_strategy()
    time.sleep(60)  # Run every 60 seconds
