from opt_gen import put, call
from opt import Option, calc_short_put_profit_loss, calc_short_call_profit_loss
from util import round_to_nearest_5, third_friday_of_next_month, calc_discounted_saving, calc_put_margin, calc_call_margin

CONTRACT_SIZE=100
STARTING_CASH=25000

class SNakedPut:
    def __init__(self):
        self.cash=STARTING_CASH
        self.option = None

    def run(self, md):
        sd = md["SPY"]
        if not self.option:
            self.buy(sd.today, sd.close, sd.iv)

        if sd.today >= self.option.expiration:
            self.sell(sd.today, sd.close)

    def buy(self, today, stock_price, iv):     
        strike = round_to_nearest_5(stock_price  * 0.90)
        expiration = third_friday_of_next_month(today)
        premium = put(today, expiration, strike, stock_price , iv)
        contract_count = int(self.cash / calc_put_margin(premium, iv, stock_price, strike))
        if contract_count > 0:
            self.option = Option(strike, premium, expiration, contract_count, CONTRACT_SIZE)
    
    def sell(self, today, stock_price):
        if self.option:
            profit_loss = calc_short_put_profit_loss(self.option, stock_price)
            self.cash+=profit_loss
            #print(today, profit_loss)
            self.option = None

    def profit_loss(self):
        return round(self.cash, 2)
    
class SShortStraddle:
    def __init__(self):
        self.cash=STARTING_CASH
        self.call = None
        self.put = None

    def _isNotOpen(self):
        return self.call == None and self.put == None

    def _isExpired(self, today):
        return self.put and today >= self.put.expiration and self.call and today >= self.call.expiration

    def run(self, md):
        sd = md["SPY"]
        if self._isNotOpen():
            self.buy(sd.today, sd.close, sd.iv)

        if self._isExpired(sd.today):
            self.sell(sd.today, sd.close)

    def buy(self, today, stock_price, iv):
        expiration = third_friday_of_next_month(today)
        split_cash = self.cash / 2

        # put
        put_strike = round_to_nearest_5(stock_price * 0.90)
        put_premium = put(today, expiration, put_strike, stock_price, iv)
        put_contract_count = int(split_cash / calc_put_margin(put_premium, iv, stock_price, put_strike))

        # call
        call_strike = round_to_nearest_5(stock_price * 1.10)
        call_premium = call(today, expiration, call_strike, stock_price, iv)
        call_contract_count = int(split_cash / calc_call_margin(call_premium, iv, stock_price, call_strike))

        # buy
        if put_contract_count > 0 and call_contract_count > 0:
            contract_count = min(put_contract_count, call_contract_count)
            self.put = Option(put_strike, put_premium, expiration, contract_count, CONTRACT_SIZE)
            self.call = Option(call_strike, call_premium, expiration, contract_count, CONTRACT_SIZE)

    
    def sell(self, today, stock_price):
        if self.put and self.call:
            profit_loss_put = calc_short_put_profit_loss(self.put, stock_price)
            self.cash+=profit_loss_put

            profit_loss_call = calc_short_call_profit_loss(self.call, stock_price)
            self.cash+=profit_loss_call

            #print(today, "put: ", int(profit_loss_put), ",call: ", int(profit_loss_call), ",total: ", int(profit_loss_put + profit_loss_call))
            self.put = None
            self.call = None

    def profit_loss(self):
        return round(self.cash, 2)

class TradingData:
    def __init__(self, today, close, iv, sma_10, macdsignal, stochslowk, stochslowd):
        self.today = today
        self.close = close
        self.iv = iv
        self.sma_10 = sma_10
        self.macdsignal = macdsignal
        self.stochslowk = stochslowk
        self.stochslowd = stochslowd





class SSaveThousandPerMonth:
    def __init__(self):
        self.cash=1000
        self.last_month_purchased=0

    def run(self, md):
        sd = md["SPY"]
        if sd.today.month != self.last_month_purchased:
            self.cash+=calc_discounted_saving(sd)
            self.last_month_purchased=sd.today.month

    def profit_loss(self):
        return round(self.cash, 2)

class SDollarCostAveraging:
    def __init__(self):
        self.cash=1000
        self.shares = 0
        self.last_close = None
        self.last_month_purchased=0

    def run(self, md):
        sd = md["SPY"]
        self.last_close = sd.close
        if sd.today.month != self.last_month_purchased:
            self.cash+=calc_discounted_saving(sd)
            self.last_month_purchased=sd.today.month
            self.buy(sd)

    def buy(self, sd):
        shares_to_purchase = int(self.cash / sd.close)
        self.cash-= shares_to_purchase * sd.close
        self.shares+= shares_to_purchase
        #print(self.__class__.__name__ + " buy", sd.today, self.shares)  

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)


class SBuyAndHold:
    def __init__(self):
        self.cash=STARTING_CASH
        self.shares = 0
        self.last_close = None

    def run(self, md):
        sd = md["SPY"]
        self.last_close = sd.close
        if self.shares == 0:
            self.buy(sd)

    def buy(self, sd):
        self.shares = int(self.cash / sd.close)
        self.cash-= self.shares * sd.close
        print(self.__class__.__name__ + " buy", sd.today, self.shares)  

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)

class SPhilTown:
    def __init__(self):
        self.cash=STARTING_CASH
        self.shares = 0
        self.last_close = None

    def _isBuy(self, sd):
        isBuyMaCrossOver = sd.close > sd.sma_10
        isBuyMacdCrossOver = sd.macdsignal > 0
        isBuyStochasticCrossOver = sd.stochslowk > sd.stochslowd
        return isBuyMaCrossOver and isBuyMacdCrossOver and isBuyStochasticCrossOver and self.shares==0
        #return isBuyMaCrossOver and self.shares==0

    def _isSell(self, sd):
        isSellMaCrossOver = sd.close < sd.sma_10
        isSellMacdCrossOver = sd.macdsignal < 0
        isSellStochasticCrossOver = sd.stochslowk < sd.stochslowd
        return isSellMaCrossOver and isSellMacdCrossOver and isSellStochasticCrossOver and self.shares!=0
        #return isSellMaCrossOver and self.shares!=0

    def run(self, md):
        sd = md["SPY"]
        self.last_close = sd.close
        if self._isBuy(sd):
            self.buy(sd)

        if self._isSell(sd):
            self.sell(sd)

    def buy(self, sd):
        self.shares = int(self.cash / sd.close)
        self.cash-= self.shares * sd.close
        #print("SPhilTown buy", sd.today, self.shares)
    
    def sell(self, sd):
        old_cash = self.cash
        self.cash+= self.shares * sd.close
        profit_loss = self.cash - old_cash
        #print(self.__class__.__name__ + " sell", sd.today, self.shares, f"${profit_loss:,.0f}")
        self.shares = 0

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)
    
class SBurry:
    def __init__(self):
        self.cash=STARTING_CASH
        self.shares = 0
        self.last_close = None
        self.watchlist = ["AMZN", "BABA", "BKNG", "BRKR", "C", "CVS", "GOOG", "HCA", "JD", "MGM", "Msd", "NXST", "ORCL", "QRTEA", "SB", "SBLK", "VTLE", "WBD"]

    def _isBuy(self, sd):
        isBuyMaCrossOver = sd.close > sd.sma_10
        isBuyMacdCrossOver = sd.macdsignal > 0
        isBuyStochasticCrossOver = sd.stochslowk > sd.stochslowd
        return isBuyMaCrossOver and isBuyMacdCrossOver and isBuyStochasticCrossOver and self.shares==0
        #return isBuyMaCrossOver and self.shares==0

    def _isSell(self, sd):
        isSellMaCrossOver = sd.close < sd.sma_10
        isSellMacdCrossOver = sd.macdsignal < 0
        isSellStochasticCrossOver = sd.stochslowk < sd.stochslowd
        return isSellMaCrossOver and isSellMacdCrossOver and isSellStochasticCrossOver and self.shares!=0
        #return isSellMaCrossOver and self.shares!=0

    def run(self, md):
        sd = md["SPY"]
        self.last_close = sd.close
        if self._isBuy(sd):
            self.buy(sd)

        if self._isSell(sd):
            self.sell(sd)

    def buy(self, sd):
        self.shares = int(self.cash / sd.close)
        self.cash-= self.shares * sd.close
        #print("SPhilTown buy", sd.today, self.shares)
    
    def sell(self, sd):
        old_cash = self.cash
        self.cash+= self.shares * sd.close
        profit_loss = self.cash - old_cash
        #print(self.__class__.__name__ + " sell", sd.today, self.shares, f"${profit_loss:,.0f}")
        self.shares = 0

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)