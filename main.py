from data_loader import load_market_data, get_symbols
from mapper import market_data_for_date
from strats import Portfolio, SNakedPut, SShortStraddle, SBuyAndHold, SDollarCostAveraging, SSaveThousandPerMonth, SPhilTown, SStockTwoHundredSMA, SForexEurUsd, SDarvas, SStockFiftySMA, LogLevel, SRsi, SStopLoss__
from util import Timer, print_results, print_results_with_portfolio

def create_single_asset_strats() -> dict:
    symbol_strat_map = {}
    for symbol in get_symbols():
        bh = SBuyAndHold(symbol)
        sl = SStopLoss__([symbol], LogLevel.NONE)
        symbol_strat_map[symbol] = [bh, sl]
    return symbol_strat_map

def main():
    t = Timer()

    df_market_data = load_market_data()
    
    df_spy = df_market_data.xs("SPY", level=1)
    
    multi_asset_strats = [
        SBuyAndHold(Portfolio.BURRY, LogLevel.NONE),
        SStopLoss__(Portfolio.BURRY, LogLevel.DEBUG)
    ]

    single_asset_strats = {}#create_single_asset_strats()

    all_strats = multi_asset_strats + list(single_asset_strats.values())

    #df_spy = df_spy.tail(215) # shorten timeseries
    for today, _ in df_spy.iterrows():
        md = market_data_for_date(today, df_market_data)
        for s in all_strats:
            s.run(md)

    print_results(df_spy, multi_asset_strats)
    print_results_with_portfolio(df_spy, single_asset_strats)
    
    t.stop()

if __name__ == "__main__":
    main()