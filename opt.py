class Option:
    def __init__(self, strike, premium, expiration, contract_count, contract_size):
        self.strike = strike
        self.premium = premium
        self.expiration = expiration
        self.contract_count = contract_count
        self.contract_size = contract_size

COMMISSION=0

# short put
def calc_short_put_profit_loss(option, underlying_price):
    return _calc_short_put_profit_loss(option.strike, underlying_price, option.premium, COMMISSION, option.contract_count, option.contract_size)

def _calc_short_put_profit_loss(strike_price, underlying_price, premium_received, transaction_fee, contract_count, contract_size):
    return ((premium_received - max(strike_price - underlying_price, 0)) * contract_size * contract_count) - transaction_fee

# short call
def calc_short_call_profit_loss(option, underlying_price):
    return _calc_short_call_profit_loss(option.strike, underlying_price, option.premium, COMMISSION, option.contract_count, option.contract_size)

def _calc_short_call_profit_loss(strike_price, underlying_price, premium_received, transaction_fee, contract_count, contract_size):
    return ((premium_received - max(underlying_price - strike_price, 0)) * contract_size * contract_count) - transaction_fee
