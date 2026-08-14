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

def get_multi_asset_strats_list():
    multi_asset_strats = [
        SBuyAndHold(['ALRM'], LogLevel.NONE),
        SStopLoss__(['ALRM'], LogLevel.DEBUG),
        SBuyAndHold(['BLD'], LogLevel.NONE),
        SStopLoss__(['BLD'], LogLevel.DEBUG),
        SBuyAndHold(['BOOT'], LogLevel.NONE),
        SStopLoss__(['BOOT'], LogLevel.DEBUG),
        SBuyAndHold(['COIN'], LogLevel.NONE),
        SStopLoss__(['COIN'], LogLevel.DEBUG),
        SBuyAndHold(['COST'], LogLevel.NONE),
        SStopLoss__(['COST'], LogLevel.DEBUG),
        SBuyAndHold(['CRAWA'], LogLevel.NONE),
        SStopLoss__(['CRAWA'], LogLevel.DEBUG),
        SBuyAndHold(['CROX'], LogLevel.NONE),
        SStopLoss__(['CROX'], LogLevel.DEBUG),
        SBuyAndHold(['CRWD'], LogLevel.NONE),
        SStopLoss__(['CRWD'], LogLevel.DEBUG),
        SBuyAndHold(['CVCO'], LogLevel.NONE),
        SStopLoss__(['CVCO'], LogLevel.DEBUG),
        SBuyAndHold(['DAC'], LogLevel.NONE),
        SStopLoss__(['DAC'], LogLevel.DEBUG),
        SBuyAndHold(['DECK'], LogLevel.NONE),
        SStopLoss__(['DECK'], LogLevel.DEBUG),
        SBuyAndHold(['EACO'], LogLevel.NONE),
        SStopLoss__(['EACO'], LogLevel.DEBUG),
        SBuyAndHold(['FIX'], LogLevel.NONE),
        SStopLoss__(['FIX'], LogLevel.DEBUG),
        SBuyAndHold(['FTLF'], LogLevel.NONE),
        SStopLoss__(['FTLF'], LogLevel.DEBUG),
        SBuyAndHold(['GOOG'], LogLevel.NONE),
        SStopLoss__(['GOOG'], LogLevel.DEBUG),
        SBuyAndHold(['KULR'], LogLevel.NONE),
        SStopLoss__(['KULR'], LogLevel.DEBUG),
        SBuyAndHold(['LEN'], LogLevel.NONE),
        SStopLoss__(['LEN'], LogLevel.DEBUG),
        SBuyAndHold(['MCFT'], LogLevel.NONE),
        SStopLoss__(['MCFT'], LogLevel.DEBUG),
        SBuyAndHold(['MNDY'], LogLevel.NONE),
        SStopLoss__(['MNDY'], LogLevel.DEBUG),
        SBuyAndHold(['NSSC'], LogLevel.NONE),
        SStopLoss__(['NSSC'], LogLevel.DEBUG),
        SBuyAndHold(['OLLI'], LogLevel.NONE),
        SStopLoss__(['OLLI'], LogLevel.DEBUG),
        SBuyAndHold(['PANW'], LogLevel.NONE),
        SStopLoss__(['PANW'], LogLevel.DEBUG),
        SBuyAndHold(['PLTR'], LogLevel.NONE),
        SStopLoss__(['PLTR'], LogLevel.DEBUG),
        SBuyAndHold(['PLUS'], LogLevel.NONE),
        SStopLoss__(['PLUS'], LogLevel.DEBUG),
        SBuyAndHold(['SBUX'], LogLevel.NONE),
        SStopLoss__(['SBUX'], LogLevel.DEBUG),
        SBuyAndHold(['SHOP'], LogLevel.NONE),
        SStopLoss__(['SHOP'], LogLevel.DEBUG),
        SBuyAndHold(['SKX'], LogLevel.NONE),
        SStopLoss__(['SKX'], LogLevel.DEBUG),
        SBuyAndHold(['SNOW'], LogLevel.NONE),
        SStopLoss__(['SNOW'], LogLevel.DEBUG),
        SBuyAndHold(['SPNS'], LogLevel.NONE),
        SStopLoss__(['SPNS'], LogLevel.DEBUG),
        SBuyAndHold(['SPY'], LogLevel.NONE),
        SStopLoss__(['SPY'], LogLevel.DEBUG),
        SBuyAndHold(['TSLA'], LogLevel.NONE),
        SStopLoss__(['TSLA'], LogLevel.DEBUG),
        SBuyAndHold(['UFPT'], LogLevel.NONE),
        SStopLoss__(['UFPT'], LogLevel.DEBUG)
    ]
    return [
        SBuyAndHold(['BTCUSD'], LogLevel.NONE),
        SStopLoss__(['BTCUSD'], LogLevel.DEBUG)
    ]

def main():
    t = Timer()

    df_market_data = load_market_data()
    
    df_spy = df_market_data.xs("SPY", level=1)
    
    multi_asset_strats = [
        SBuyAndHold(Portfolio.SPY, LogLevel.NONE),
        SStopLoss__(Portfolio.SPY, LogLevel.DEBUG)
    ]

    multi_asset_strats = get_multi_asset_strats_list()

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