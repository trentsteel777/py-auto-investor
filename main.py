from data_loader import load_market_data
from mapper import market_data_for_date
from strats import Portfolio, SNakedPut, SShortStraddle, SBuyAndHold, SDollarCostAveraging, SSaveThousandPerMonth, SPhilTown, SStockTwoHundredSMA
from util import Timer, print_results

def main():
    t = Timer()

    df_market_data = load_market_data()
    
    df_spy = df_market_data.xs("SPY", level=1)
    
    strats = [ 
        # Option strategies
        SNakedPut(), 
        SShortStraddle(), 

        # Stock strategies
        SPhilTown(Portfolio.SPY),
        SPhilTown(Portfolio.BURRY), 
        SPhilTown(Portfolio.GREENBLAT),
        SStockTwoHundredSMA(Portfolio.GREENBLAT),
        SStockTwoHundredSMA(Portfolio.SPY),

        # Benchmark strategies
        SBuyAndHold(),
        SSaveThousandPerMonth(), 
        SDollarCostAveraging() 
    ]

    for today, _ in df_spy.iterrows():
        md = market_data_for_date(today, df_market_data)
        for s in strats:
            s.run(md)

    print_results(df_spy, strats)

    t.stop()


if __name__ == "__main__":
    main()