import pandas as pd
import numpy as np
import talib
import os
from util import dotdict

DATA_DIR='data'


class DailyMarketData:
    def __init__(self, today, df_today):
        self.today = today
        self.data = {}
        for symbol, row in df_today.iterrows():
            d = dotdict(row)
            d['symbol'] = symbol
            self.data[symbol] = d

    def get(self, symbol):
        return self.data.get(symbol)

def market_data_for_date(today, df_market_data):
    data = df_market_data.loc[today]
    return DailyMarketData(today, data)

def calculate_daily_returns(prices):
    """
    Calculate daily returns from a series of stock prices.

    Args:
    - prices: A pandas DataFrame with 'Date' and 'close' columns.

    Returns:
    - A pandas DataFrame with 'Date' and 'Daily Return' columns.
    """
    # Calculate the daily returns
    prices['daily_return'] = prices['close'].pct_change()

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
    returns['historical_volatility'] = returns['daily_return'].rolling(window=window).std()
    
    # Calculate the annualized volatility (assuming 252 trading days in a year)
    returns['annualized_volatility'] = returns['historical_volatility'] * np.sqrt(252)

    returns['iv'] = returns['annualized_volatility'] * 2

    return returns

def calculate_macd(df):
    df['macdfast'], df['macdslow'], df['macdsignal'] = talib.MACD(df['close'], fastperiod=8, slowperiod=17, signalperiod=9)
    return df

def calculate_stochastic(df):
    df['stochslowk'], df['stochslowd'] = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=14, slowk_period=5, slowd_period=5)
    return df

def calculate_moving_average(df):
    df['sma_10'] = talib.SMA(df['close'], timeperiod=10)
    df['sma_200'] = talib.SMA(df['close'], timeperiod=200)
    return df

def rename_columns(df):
    nc = dict(zip(df.columns, [ c.lower() for c in df.columns]))
    df = df.rename(columns = nc)
    
    df['close'] = df['adj close']
    df.drop(columns=['adj close'])

    return df

def load_symbol_data(file_name):
    if not file_name.endswith(".csv"):
        file_name+=".csv"

    file_path = f'{DATA_DIR}/{file_name}'

    df = pd.read_csv(file_path, parse_dates=['Date'], date_format='%d/%m/%Y')
    
    df = rename_columns(df)

    df['date'] = pd.to_datetime(df['date'])
    
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
        df["symbol"] = symbol
        df_master = pd.concat([df_master, df], ignore_index=True)
    df_master.set_index(['date', 'symbol'], inplace=True)
    return df_master
