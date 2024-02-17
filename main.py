from hist_vol import share_prices_with_hv, load_market_data, load_single_market_data
from strats import SNakedPut, SShortStraddle, SPhilTown, TradingData, SBuyAndHold, SDollarCostAveraging, SSaveThousandPerMonth
from util import Timer

def print_results(df, strats):
    start_date = df.iloc[0]['Date'].to_pydatetime().date()
    end_date = df.iloc[-1]['Date'].to_pydatetime().date()
    print("start_date:", start_date, "-> end_date:", end_date)
    for s in strats:
        print(f"{s.__class__.__name__ :<15}:", f"${s.profit_loss():,.0f}")

def market_data(df_stock_data, row):
    market_data = {}
    today = row["Date"]
    for symbol, data in df_stock_data.items():
        row = data.loc[data["Date"] == today]
        if len(row) == 1:
            row = row.iloc[0]
            market_data[symbol] = stock_data(row)
        elif len(row) > 1:
            raise Exception("More than one date found")
    return market_data

def stock_data(row):
    today = row["Date"].to_pydatetime().date()
    close = row["Adj Close"]
    iv = row["Annualized Volatility"] * 2
    sma_10 = row['sma_10']
    macdsignal = row['macdsignal']
    stochslowk = row['stochslowk']
    stochslowd = row['stochslowd']
    return TradingData(today, close, iv, sma_10, macdsignal, stochslowk, stochslowd)

def main():
    t = Timer()

    #df_stock_data = load_market_data()
    df_stock_data = load_single_market_data("SPY")
    df = df_stock_data["SPY"]
    df = df.iloc[20:]
    
    strats = [ SNakedPut(), SShortStraddle(), SPhilTown(), SBuyAndHold(), SDollarCostAveraging(), SSaveThousandPerMonth() ]
    for index, row in df.iterrows():
        md = market_data(df_stock_data, row)
        for s in strats:
            s.run(md)

    print_results(df, strats)

    t.stop()


if __name__ == "__main__":
    main()