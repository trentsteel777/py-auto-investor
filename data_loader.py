import pandas as pd
import numpy as np
import talib
import os

DATA_DIR='data'

class SymbolData:
    def __init__(self, today, close, iv, sma_10, macdsignal, stochslowk, stochslowd):
        self.today = today
        self.close = close
        self.iv = iv
        self.sma_10 = sma_10
        self.macdsignal = macdsignal
        self.stochslowk = stochslowk
        self.stochslowd = stochslowd

def market_data_for_date(today, df_market_data):
    market_data = {}
    for symbol, row in df_market_data.loc[today].iterrows():
        market_data[symbol] = symbol_data(today, row)
    return market_data

def symbol_data(today, row):
    today = today.to_pydatetime().date()
    close = row["Adj Close"]
    iv = row["Annualized Volatility"] * 2
    sma_10 = row['sma_10']
    macdsignal = row['macdsignal']
    stochslowk = row['stochslowk']
    stochslowd = row['stochslowd']
    return SymbolData(today, close, iv, sma_10, macdsignal, stochslowk, stochslowd)


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

def load_symbol_data(file_name):
    if not file_name.endswith(".csv"):
        file_name+=".csv"

    file_path = f'{DATA_DIR}/{file_name}'

    df = pd.read_csv(file_path, parse_dates=['Date'], date_format='%d/%m/%Y')
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df = calculate_daily_returns(df)

    df = calculate_historical_volatility(df, window=20)

    df = calculate_macd(df)

    df = calculate_stochastic(df)

    df = calculate_moving_average(df)

    return df


def load_market_data():
    df_master = pd.DataFrame()
    files = os.listdir(DATA_DIR)
    for f in files:
        symbol = f.replace(".csv", "")
        df = load_symbol_data(f)
        df["SYMBOL"] = symbol
        df_master = pd.concat([df_master, df], ignore_index=True)
    df_master.set_index(['Date', 'SYMBOL'], inplace=True)
    return df_master
