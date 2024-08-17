from data_loader import load_market_data, get_symbols
from mapper import market_data_for_date
from strats import Portfolio, SNakedPut, SShortStraddle, SBuyAndHold, SDollarCostAveraging, SSaveThousandPerMonth, SPhilTown, SStockTwoHundredSMA, SForexEurUsd, SDarvas, SStockFiftySMA, LogLevel, SRsi, SStopLoss__
from util import Timer, print_results, print_results_with_portfolio, CPortfolio

def create_symbol_strat_map(strats) -> dict:
    symbol_strat_map = {}
    for symbol in get_symbols():
        bh = SBuyAndHold(symbol)
        sl = SStopLoss__(CPortfolio([symbol]), LogLevel.NONE)

        symbol_strat_map[symbol] = [bh, sl]
        strats.append(bh)
        strats.append(sl)
    return symbol_strat_map

def main():
    t = Timer()

    df_market_data = load_market_data()
    
    df_spy = df_market_data.xs("SPY", level=1)
    
    strats = [
        # Option strategies
        #SNakedPut(), 
        #SShortStraddle(), 

        # Stock strategies
        #SPhilTown(Portfolio.SPY),
        #SPhilTown(Portfolio.BURRY), 
        #SPhilTown(Portfolio.GREENBLAT),
        #SStockTwoHundredSMA(Portfolio.GREENBLAT),
        #SStockTwoHundredSMA(Portfolio.SPY),

        # Forex strategies
        # SForexEurUsd(Portfolio.EURUSD),

        # Benchmark strategies
        #SStockFiftySMA(Portfolio.SPY, LogLevel.NONE),
        #SBuyAndHold("SPY"),
        #SSaveThousandPerMonth(), 
        #SDollarCostAveraging(),

        #SDarvas(Portfolio.SPY, LogLevel.DEBUG),
    ]

    symbol_strat_map = create_symbol_strat_map(strats)

    #df_spy = df_spy.tail(215) # shorten timeseries
    for today, _ in df_spy.iterrows():
        md = market_data_for_date(today, df_market_data)
        for s in strats:
            s.run(md)

    print_results_with_portfolio(df_spy, symbol_strat_map)
    
    t.stop()

if __name__ == "__main__":
    main()