from util import dotdict

class DailyMarketData:
    def __init__(self, today, df_today):
        self.today = today
        self.data = {}
        for symbol, row in df_today.iterrows():
            d = dotdict(row)
            d['symbol'] = symbol
            self.data[symbol] = d

    def get(self, symbol):
        return self.data.get(symbol)

def market_data_for_date(today, df_market_data):
    data = df_market_data.loc[today]
    return DailyMarketData(today, data)