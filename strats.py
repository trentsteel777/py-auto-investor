from opt_gen import put, call
from opt import Option, calc_short_put_profit_loss, calc_short_call_profit_loss
from util import round_to_nearest_5, third_friday_of_next_month

CONTRACT_SIZE=100

class SNakedPut:
    def __init__(self):
        self.contract_count=10
        self.option = None
        self.profit_loss_list = []

    def run(self, today, stock_price, iv):
        if not self.option:
            self.buy(today, stock_price, iv)

        if today >= self.option.expiration:
            self.sell(today, stock_price)

    def buy(self, today, stock_price, iv):
        strike = round_to_nearest_5(stock_price * 0.90)
        expiration = third_friday_of_next_month(today)
        premium = put(today, expiration, strike, stock_price, iv)
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

    def run(self, today, stock_price, iv):
        if self._isNotOpen():
            self.buy(today, stock_price, iv)

        if self._isExpired(today):
            self.sell(today, stock_price)

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