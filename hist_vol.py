import pandas as pd
import numpy as np
import talib
import os

DATA_DIR='data'

def calculate_daily_returns(prices):
    """
    Calculate daily returns from a series of stock prices.

    Args:
    - prices: A pandas DataFrame with 'Date' and 'Adj Close' columns.

    Returns:
    - A pandas DataFrame with 'Date' and 'Daily Return' columns.
    """
    # Calculate the daily returns
    prices['Daily Return'] = prices['Adj Close'].pct_change()

    return prices

def calculate_historical_volatility(returns, window=20):
    """
    Calculate historical volatility from a series of returns.

    Args:
    - returns: A pandas DataFrame with 'Date' and 'Daily Return' columns.
    - window: Rolling window size for calculating historical volatility.

    Returns:
    - A pandas DataFrame with 'Date' and 'Historical Volatility' columns.
    """
    # Calculate the rolling standard deviation of returns
    returns['Historical Volatility'] = returns['Daily Return'].rolling(window=window).std()
    
    # Calculate the annualized volatility (assuming 252 trading days in a year)
    returns['Annualized Volatility'] = returns['Historical Volatility'] * np.sqrt(252)

    return returns

def calculate_macd(df):
    df['macdfast'], df['macdslow'], df['macdsignal'] = talib.MACD(df['Adj Close'], fastperiod=8, slowperiod=17, signalperiod=9)
    return df

def calculate_stochastic(df):
    df['stochslowk'], df['stochslowd'] = talib.STOCH(df['High'], df['Low'], df['Adj Close'], fastk_period=14, slowk_period=5, slowd_period=5)
    return df

def calculate_moving_average(df):
    df['sma_10'] = talib.SMA(df['Adj Close'], timeperiod=10)
    return df

def share_prices_with_hv(file_name):
    if not file_name.endswith(".csv"):
        file_name+=".csv"

    # Read the CSV file into a pandas DataFrame
    file_path = f'{DATA_DIR}/{file_name}'  # Replace with the actual file path
    spy_prices = pd.read_csv(file_path, parse_dates=['Date'])

    # Calculate daily returns
    spy_prices = calculate_daily_returns(spy_prices)

    # Calculate historical volatility (using a 20-day window as an example)
    spy_prices = calculate_historical_volatility(spy_prices, window=20)

    spy_prices = calculate_macd(spy_prices)

    spy_prices = calculate_stochastic(spy_prices)

    spy_prices = calculate_moving_average(spy_prices)
    # Display the result
    #print(spy_prices[['Date', 'Daily Return', 'Historical Volatility', 'Annualized Volatility']])
    return spy_prices


def load_market_data():
    df_master = pd.DataFrame()
    files = os.listdir(DATA_DIR)
    for f in files:
        symbol = f.replace(".csv", "")
        df = share_prices_with_hv(f)
        df["SYMBOL"] = symbol
        df_master = pd.concat([df_master, df], ignore_index=True)
    df_master.set_index(['Date', 'SYMBOL'], inplace=True)
    return df_master
