import pandas as pd
import QuantLib as ql

switcher = {
    1: ql.January,
    2: ql.February,
    3: ql.March,
    4: ql.April,
    5: ql.May,
    6: ql.June,
    7: ql.July,
    8: ql.August,
    9: ql.September,
    10: ql.October,
    11: ql.November,
    12: ql.December
}
def ql_month(date):
    return switcher.get(date.month)


def option(option_type, today, expiration, strike, stock_price, iv):
    todaysDate = ql.Date(today.day, ql_month(today), today.year)
    ql.Settings.instance().evaluationDate = todaysDate
    exercise = ql.AmericanExercise(todaysDate, ql.Date(expiration.day, ql_month(expiration), expiration.year))
    payoff = ql.PlainVanillaPayoff(option_type, strike)
    option = ql.VanillaOption(payoff, exercise)
    underlying = ql.SimpleQuote(stock_price)
    #calendar =  ql.UnitedStates(ql.UnitedStates.NYSE)
    dividendYield = ql.FlatForward(todaysDate, 0.00, ql.Actual365Fixed())
    volatility = ql.BlackConstantVol(todaysDate, ql.TARGET(), iv, ql.Actual365Fixed())
    riskFreeRate = ql.FlatForward(todaysDate, 0.05, ql.Actual365Fixed())
    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(underlying),
        ql.YieldTermStructureHandle(dividendYield),
        ql.YieldTermStructureHandle(riskFreeRate),
        ql.BlackVolTermStructureHandle(volatility),
    )
    results = []
    option.setPricingEngine(ql.BjerksundStenslandApproximationEngine(process))
    option_price = option.NPV()
    results.append(("Bjerksund-Stensland", option_price))
    df = pd.DataFrame(results, columns=["Method", "Option value"])
    df.style.hide(axis="index")

    #print(df)

    return option_price

def put(today, expiration, strike, stock_price, iv):
    return option(ql.Option.Put, today, expiration, strike, stock_price, iv)

def call(today, expiration, strike, stock_price, iv):
    return option(ql.Option.Call, today, expiration, strike, stock_price, iv)
