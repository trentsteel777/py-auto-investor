
import os
import pandas as pd
from datetime import datetime, timedelta

folder_path = r"hist_data"

today = datetime.strptime("2016-06-01", "%Y-%m-%d") # datetime.today()
today_formatted = today.strftime('%Y-%m-%d')

def load_csv_files(folder_path):
    dataframes = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.startswith("UnderlyingOptionsEODQuotes_") and file.endswith(".csv"):
                file_date = file.split("_")[1].split(".")[0]
                if file_date == today_formatted:
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    dataframes.append(df)

    return dataframes

def filter_next_months_puts(df):
    # Convert date strings to datetime objects
    df['quote_date'] = pd.to_datetime(df['quote_date'])
    df['expiration'] = pd.to_datetime(df['expiration'])

    # Get the next month
    next_month = today.replace(day=1) + timedelta(days=32)

    # Filter for next month's expiration
    next_month_options = df[df['expiration'].dt.month == next_month.month]

    # Filter for put options
    puts_only = next_month_options[next_month_options['option_type'] == 'P']

    return puts_only

def filter_20_30_percent_of_stock_price(puts_only):
    column_index = puts_only.columns.get_loc("underlying_ask_eod")
    stock_price = puts_only.iloc[0, column_index]
    
    # Calculate the range of strike prices
    lower_bound = stock_price * 0.7  # 20% below the stock price
    upper_bound = stock_price * 0.8  # 30% below the stock price

    # Filter the puts_only DataFrame for options within the specified range
    selected_puts = puts_only[(puts_only['strike'] >= lower_bound) & (puts_only['strike'] <= upper_bound)]

    return selected_puts

def average_monthly_historical_volatility():
    df = calc_hv()[["Date","Adj Close"]]
    df.set_index('Date', inplace=True)

    # Calculate daily returns
    df['Daily_Return'] = df['Adj Close'].pct_change()

    # Group by month and calculate standard deviation of daily returns
    monthly_volatility = df.groupby(pd.Grouper(freq='M'))['Daily_Return'].std()

    # Calculate the average monthly volatility
    average_monthly_volatility = monthly_volatility.mean()

    print("Monthly Historical Volatility:")
    print(monthly_volatility)
    print("\nAverage Monthly Historical Volatility:", average_monthly_volatility)


def calc_future_value():
    initial_investment = 1000  # Initial investment amount
    monthly_investment = 1000  # Annual investment amount
    months = 30 * 12           # Number of months
    annual_return = 0.00583    # Average annual return after inflation

    future_value = initial_investment  # Initialize future value

    for year in range(months):
        future_value *= 1 + annual_return
        future_value += monthly_investment

    print("Future value after", months, "months of dollar-cost averaging:",  f"${round(future_value, 2):,.0f}")
