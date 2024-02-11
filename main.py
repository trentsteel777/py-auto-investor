from hist_vol import share_prices_with_hv
from strats import SNakedPut, SShortStraddle
from util import Timer

def print_results(strats):
    for s in strats:
        print(f"{s.__class__.__name__ :<15}:", f"${s.profit_loss():,.0f}")

def main():
    t = Timer()
    df = share_prices_with_hv("SPY")
    df = df.iloc[20:]

    strats = [ SNakedPut(), SShortStraddle() ]
    for index, row in df.iterrows():
        today, close, iv = row["Date"].to_pydatetime().date(), row["Adj Close"], row["Annualized Volatility"] * 2
        for s in strats:
            s.run(today, close, iv)

    print_results(strats)

    t.stop()

if __name__ == "__main__":
    main()
    


