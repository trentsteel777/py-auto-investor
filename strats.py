from datetime import date

from opt_gen import put, call
from opt import Option, calc_short_put_profit_loss, calc_short_call_profit_loss
from util import round_to_nearest_5, third_friday_of_next_month

CONTRACT_SIZE=100
STARTING_CASH=25000

class SNakedPut:
    def __init__(self):
        self.contract_count=10
        self.option = None
        self.profit_loss_list = []

    def run(self, td):
        if not self.option:
            self.buy(td.today, td.close, td.iv)

        if td.today >= self.option.expiration:
            self.sell(td.today, td.close)

    def buy(self, today, stock_price, iv):
        strike = round_to_nearest_5(stock_price  * 0.90)
        expiration = third_friday_of_next_month(today)
        premium = put(today, expiration, strike, stock_price , iv)
        self.option = Option(strike, premium, expiration, self.contract_count, CONTRACT_SIZE)
    
    def sell(self, today, stock_price):
        profit_loss = calc_short_put_profit_loss(self.option, stock_price)
        self.profit_loss_list.append(profit_loss)
        #print(today, profit_loss)
        self.option = None

    def profit_loss(self):
        return round(sum(self.profit_loss_list), 2)
    
class SShortStraddle:
    def __init__(self):
        self.contract_count=5
        self.call = None
        self.put = None
        self.profit_loss_list = []

    def _isNotOpen(self):
        return self.call == None and self.put == None

    def _isExpired(self, today):
        return today >= self.put.expiration and today >= self.call.expiration

    def run(self, td):
        if self._isNotOpen():
            self.buy(td.today, td.close, td.iv)

        if self._isExpired(td.today):
            self.sell(td.today, td.close)

    def buy(self, today, stock_price, iv):
        expiration = third_friday_of_next_month(today)

        # put
        strike = round_to_nearest_5(stock_price * 0.90)
        premium = put(today, expiration, strike, stock_price, iv)
        self.put = Option(strike, premium, expiration, self.contract_count, CONTRACT_SIZE)

        # call
        strike = round_to_nearest_5(stock_price * 1.10)
        premium = call(today, expiration, strike, stock_price, iv)
        self.call = Option(strike, premium, expiration, self.contract_count, CONTRACT_SIZE)

    
    def sell(self, today, stock_price):
        profit_loss_put = calc_short_put_profit_loss(self.put, stock_price)
        self.profit_loss_list.append(profit_loss_put)

        profit_loss_call = calc_short_call_profit_loss(self.call, stock_price)
        self.profit_loss_list.append(profit_loss_call)

        #print(today, "put: ", int(profit_loss_put), ",call: ", int(profit_loss_call), ",total: ", int(profit_loss_put + profit_loss_call))
        self.put = None
        self.call = None

    def profit_loss(self):
        return round(sum(self.profit_loss_list), 2)

class TradingData:
    def __init__(self, today, close, iv, sma_10, macdsignal, stochslowk, stochslowd):
        self.today = today
        self.close = close
        self.iv = iv
        self.sma_10 = sma_10
        self.macdsignal = macdsignal
        self.stochslowk = stochslowk
        self.stochslowd = stochslowd

#https://www.macrotrends.net/countries/USA/united-states/inflation-rate-cpi#google_vignette
inflation_data = {
    1990: 5.398,
    1991: 4.235,
    1992: 3.0288,
    1993: 2.9517,
    1994: 2.6074,
    1995: 2.8054,
    1996: 2.9312,
    1997: 2.3377,
    1998: 1.5523,
    1999: 2.188,
    2000: 3.3769,
    2001: 2.8262,
    2002: 1.586,
    2003: 2.2701,
    2004: 2.6772,
    2005: 3.3927,
    2006: 3.2259,
    2007: 2.8527,
    2008: 3.8391,
    2009: -0.3555,
    2010: 1.64,
    2011: 3.1568,
    2012: 2.0693,
    2013: 1.4648,
    2014: 1.6222,
    2015: 0.1186,
    2016: 1.2616,
    2017: 2.1301,
    2018: 2.4426,
    2019: 1.8122,
    2020: 1.2336,
    2021: 4.6979,
    2022: 8.0028,
    2023: 8.0028,
    2024: 8.0028,
}


def calc_discounted_saving(td):
    future_value = 1000                       # Future value (amount to be discounted)
    years = date.today().year - td.today.year # Number of years
    r = inflation_data[td.today.year] / 100   
    discount_rate = r                         # Average annual inflation rate

    present_value = future_value / (1 + discount_rate) ** years

    print("Present value after", years, "years:", round(present_value, 2))

    return present_value



class SSaveThousandPerMonth:
    def __init__(self):
        self.cash=1000
        self.last_month_purchased=0

    def run(self, td):
        if td.today.month != self.last_month_purchased:
            self.cash+=calc_discounted_saving(td)
            self.last_month_purchased=td.today.month

    def profit_loss(self):
        return round(self.cash, 2)

class SDollarCostAveraging:
    def __init__(self):
        self.cash=1000
        self.shares = 0
        self.last_close = None
        self.last_month_purchased=0

    def run(self, td):
        self.last_close = td.close
        if td.today.month != self.last_month_purchased:
            self.cash+=calc_discounted_saving(td)
            self.last_month_purchased=td.today.month
            self.buy(td)

    def buy(self, td):
        shares_to_purchase = int(self.cash / td.close)
        self.cash-= shares_to_purchase * td.close
        self.shares+= shares_to_purchase
        #print(self.__class__.__name__ + " buy", td.today, self.shares)  

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)


class SBuyAndHold:
    def __init__(self):
        self.cash=STARTING_CASH
        self.shares = 0
        self.last_close = None

    def run(self, td):
        self.last_close = td.close
        if self.shares == 0:
            self.buy(td)

    def buy(self, td):
        self.shares = int(self.cash / td.close)
        self.cash-= self.shares * td.close
        print(self.__class__.__name__ + " buy", td.today, self.shares)  

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)

class SPhilTown:
    def __init__(self):
        self.cash=STARTING_CASH
        self.shares = 0
        self.last_close = None

    def _isBuy(self, td):
        isBuyMaCrossOver = td.close > td.sma_10
        isBuyMacdCrossOver = td.macdsignal > 0
        isBuyStochasticCrossOver = td.stochslowk > td.stochslowd
        return isBuyMaCrossOver and isBuyMacdCrossOver and isBuyStochasticCrossOver and self.shares==0
        #return isBuyMaCrossOver and self.shares==0

    def _isSell(self, td):
        isSellMaCrossOver = td.close < td.sma_10
        isSellMacdCrossOver = td.macdsignal < 0
        isSellStochasticCrossOver = td.stochslowk < td.stochslowd
        return isSellMaCrossOver and isSellMacdCrossOver and isSellStochasticCrossOver and self.shares!=0
        #return isSellMaCrossOver and self.shares!=0

    def run(self, td):
        self.last_close = td.close
        if self._isBuy(td):
            self.buy(td)

        if self._isSell(td):
            self.sell(td)

    def buy(self, td):
        self.shares = int(self.cash / td.close)
        self.cash-= self.shares * td.close
        #print("SPhilTown buy", td.today, self.shares)
    
    def sell(self, td):
        old_cash = self.cash
        self.cash+= self.shares * td.close
        profit_loss = self.cash - old_cash
        #print(self.__class__.__name__ + " sell", td.today, self.shares, f"${profit_loss:,.0f}")
        self.shares = 0

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)