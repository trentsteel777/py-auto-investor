import pandas as pd
import numpy as np

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

def share_prices_with_hv(symbol):
    # Read the CSV file into a pandas DataFrame
    file_path = f'data/{symbol}.csv'  # Replace with the actual file path
    spy_prices = pd.read_csv(file_path, parse_dates=['Date'])

    # Calculate daily returns
    spy_prices = calculate_daily_returns(spy_prices)

    # Calculate historical volatility (using a 20-day window as an example)
    spy_prices = calculate_historical_volatility(spy_prices, window=20)

    # Display the result
    #print(spy_prices[['Date', 'Daily Return', 'Historical Volatility', 'Annualized Volatility']])
    return spy_prices

