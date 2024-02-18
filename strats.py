from opt_pricer import put, call
from opt import Option, calc_short_put_profit_loss, calc_short_call_profit_loss
from util import round_to_nearest_5, third_friday_of_next_month, calc_discounted_saving, calc_put_margin, calc_call_margin
from enum import Enum, auto
from overrides import override
from abc import ABC, abstractmethod

CONTRACT_SIZE=100
STARTING_CASH=25000

# SO: Option strategies

class SNakedPut:
    def __init__(self):
        self.cash=STARTING_CASH
        self.option = None

    def run(self, md):
        sd = md.get("SPY")

        if self.option and md.today >= self.option.expiration:
            self.sell(md.today, sd.close)

        if not self.option and sd.iv > 0:
            self.buy(md.today, sd.close, sd.iv)

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

    def _isNotOpen(self, iv):
        return self.call == None and self.put == None and iv > 0

    def _isExpired(self, today):
        return self.put and today >= self.put.expiration and self.call and today >= self.call.expiration

    def run(self, md):
        sd = md.get("SPY")

        if self._isExpired(md.today):
            self.sell(md.today, sd.close)

        if self._isNotOpen(sd.iv):
            self.buy(md.today, sd.close, sd.iv)


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

# EO: Option strategies

# SO: Benchmark strategies

class SSaveThousandPerMonth:
    def __init__(self):
        self.cash=1000
        self.last_month_purchased=0

    def run(self, md):
        sd = md.get("SPY")
        if md.today.month != self.last_month_purchased:
            self.cash+=calc_discounted_saving(md.today)
            self.last_month_purchased=md.today.month

    def profit_loss(self):
        return round(self.cash, 2)

class SDollarCostAveraging:
    def __init__(self):
        self.cash=1000
        self.shares = 0
        self.last_close = None
        self.last_month_purchased=0

    def run(self, md):
        sd = md.get("SPY")
        self.last_close = sd.close
        if md.today.month != self.last_month_purchased:
            self.cash+=calc_discounted_saving(md.today)
            self.last_month_purchased=md.today.month
            self.buy(sd)

    def buy(self, sd):
        shares_to_purchase = int(self.cash / sd.close)
        self.cash-= shares_to_purchase * sd.close
        self.shares+= shares_to_purchase
        #print(self.__class__.__name__ + " buy", md.today, self.shares)  

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)


class SBuyAndHold:
    def __init__(self):
        self.cash=STARTING_CASH
        self.shares = 0
        self.last_close = None

    def run(self, md):
        sd = md.get("SPY")
        self.last_close = sd.close
        if self.shares == 0:
            self.buy(md.today, sd)

    def buy(self, today, sd):
        self.shares = int(self.cash / sd.close)
        self.cash-= self.shares * sd.close
        print(self.__class__.__name__ + " buy", today, self.shares)  

    def profit_loss(self):
        return round(self.cash + (self.shares * self.last_close), 2)

# EO: Benchmark strategies

# SO: Stock strategies

class Portfolio(Enum):
    # Michael Burry - https://twitter.com/burrytracker/status/1691435571783090176
    BURRY = ["AMZN", "BABA", "BKNG", "BRKR", "C", "CVS", "GOOG", "HCA", "JD", "MGM", "MTD", "NXST", "ORCL", "QRTEA", "SB", "SBLK", "VTLE", "WBD"]

    # Joel Greenblatt - https://www.magicformulainvesting.com/Screening/StockScreening
    GREENBLAT = ['AMCX', 'ASRT', 'BKE', 'BTMD', 'CCSI', 'COLL', 'CPRX', 'CROX', 'HPQ', 'HRMY', 'HSII', 'IMMR', 'JAKK', 'JILL', 'MCFT', 'MD', 'MED', 'MO', 'OCUP', 'PLTK', 'PRDO', 'RMNI', 'SCYX', 'SPRO', 'SURG', 'TZOO', 'UIS', 'UNTC', 'VYGR', 'ZYME']

    SPY = ['SPY']

    EURUSD = ['EURUSD']

class LogLevel(Enum):
    DEBUG = auto()
    NONE = auto()
 
class SStock(ABC):
    def __init__(self, watchlist, log_level=LogLevel.NONE):
        self.cash=STARTING_CASH
        self.shares = {}
        self.last_closes = {}
        self.watchlist = watchlist.value
        self.log_level = log_level
        
        for w in self.watchlist:
            self.shares[w] = 0
    
    @abstractmethod
    def _isBuy(self, sd):
        pass

    @abstractmethod
    def _isSell(self, sd):
        pass

    def run(self, md):
        buys = []
        for w in self.watchlist:
            sd = md.get(w)
            if sd:
                self.last_closes[w] = sd.close

                if self._isSell(sd):
                    self.sell(md.today, sd)

                if self._isBuy(sd):
                    buys.append(sd)
        
        if len(buys) > 0:
            cash_per_stock = self.cash / len(buys)
            for sd in buys:
                self.buy(md.today, sd, cash_per_stock)

    def buy(self, today, sd, cash_per_stock):
        shares = int(cash_per_stock / sd.close)
        if shares > 0:
            self.shares[sd.symbol]+= shares
            self.cash-= shares * sd.close
            #if symbol == "GOOG":
            if LogLevel.DEBUG == self.log_level:
                print(self.__class__.__name__, today, sd.symbol, ":", shares, ":", round(sd.close,2), ":", round(shares * sd.close,2))
    
    def sell(self, today, sd):
        shares = self.shares[sd.symbol]
        self.cash+= shares * sd.close
        self.shares[sd.symbol] = 0
        #if symbol == "GOOG":
        if LogLevel.DEBUG == self.log_level:
            print(self.__class__.__name__, today, sd.symbol, ":", -shares, ":", round(sd.close,2), ":", round(shares * sd.close,2))

    def profit_loss(self):
        share_values = [v * self.last_closes[k] for k,v in self.shares.items()]
        portfolio_value=sum(share_values)
        return round(self.cash + portfolio_value, 2)
    
class SPhilTown(SStock):
    def __init__(self, watchlist, log_level=LogLevel.NONE):
        super().__init__(watchlist, log_level)

    @override
    def _isBuy(self, sd):
        isBuyMaCrossOver = sd.close > sd.sma_10
        isBuyMacdCrossOver = sd.macdsignal > 0
        isBuyStochasticCrossOver = sd.stochslowk > sd.stochslowd
        return isBuyMaCrossOver and isBuyMacdCrossOver and isBuyStochasticCrossOver
    
    @override
    def _isSell(self, sd):
        isSellMaCrossOver = sd.close < sd.sma_10
        isSellMacdCrossOver = sd.macdsignal < 0
        isSellStochasticCrossOver = sd.stochslowk < sd.stochslowd
        return isSellMaCrossOver and isSellMacdCrossOver and isSellStochasticCrossOver and self.shares[sd.symbol] > 0


class SStockTwoHundredSMA(SStock):
    def __init__(self, watchlist, log_level=LogLevel.NONE):
        super().__init__(watchlist, log_level)

    @override
    def _isBuy(self, sd):
        isBuyMaCrossOver = sd.close > sd.sma_10 and sd.sma_10 > sd.sma_200
        return isBuyMaCrossOver

    @override
    def _isSell(self, sd):
        isSellMaCrossOver = sd.close < sd.sma_10 and sd.sma_10 < sd.sma_200
        return isSellMaCrossOver and self.shares[sd.symbol] > 0

# EO: Stock strategies
    
# SO: Forex strategies
class SForexEurUsd(SStock):
    def __init__(self, watchlist, log_level=LogLevel.NONE):
        super().__init__(watchlist, log_level)

    @override
    def _isBuy(self, sd):
        isBuyMaCrossOver = sd.close > sd.sma_10
        return isBuyMaCrossOver

    @override
    def _isSell(self, sd):
        isSellMaCrossOver = sd.close < sd.sma_10
        return isSellMaCrossOver and self.shares[sd.symbol] > 0
# SO: Forex strategies