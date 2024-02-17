from hist_vol import share_prices_with_hv, load_market_data
from strats import SNakedPut, SShortStraddle, SPhilTownSpy, SymbolData, SBuyAndHold, SDollarCostAveraging, SSaveThousandPerMonth, SBurry
from util import Timer

def print_results(df_spy, strats):
    start_date = df_spy.index.min().to_pydatetime().date()
    end_date = df_spy.index.max().to_pydatetime().date()
    print("start_date:", start_date, "-> end_date:", end_date)
    for s in strats:
        print(f"{s.__class__.__name__ :<15}:", f"${s.profit_loss():,.0f}")

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

def main():
    t = Timer()

    df_market_data = load_market_data()
    
    df_spy = df_market_data.xs("SPY", level=1)
    
    strats = [ 
        SNakedPut(), SShortStraddle(), SPhilTownSpy(),  SBurry(),
        SSaveThousandPerMonth(), SBuyAndHold(), SDollarCostAveraging() 
    ]

    for today, _ in df_spy.iterrows():
        md = market_data_for_date(today, df_market_data)
        for s in strats:
            s.run(md)

    print_results(df_spy, strats)

    t.stop()


if __name__ == "__main__":
    main()