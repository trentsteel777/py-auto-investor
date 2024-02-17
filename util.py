from datetime import datetime, timedelta, date
import time

def round_to_nearest_5(num):
    return round(num / 5) * 5

def third_friday_of_next_month(date):
    # Calculate the first day of next month
    first_day_of_next_month = datetime(date.year if date.month < 12 else date.year + 1, (date.month % 12) + 1, 1)

    # Calculate the weekday of the first day of next month
    first_day_weekday = first_day_of_next_month.weekday()

    # Calculate the number of days to the third Friday
    days_to_third_friday = (4 - first_day_weekday) % 7 + 14

    # Calculate the third Friday of next month
    third_friday_of_next_month = first_day_of_next_month + timedelta(days=days_to_third_friday)

    return third_friday_of_next_month.date()


class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None

    def stop(self):
        self.end_time = time.time()
        execution_time = round(self.end_time - self.start_time, 2)
        print("Execution time:", execution_time, "seconds")

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

    #print("Present value after", years, "years:", round(present_value, 2))

    return present_value

# ABN AMRO - https://www.abnamro.nl/en/media/Formulas_for_margin_calculation_tcm18-43021.pdf
def calc_call_margin(prem, vol, stock_price, strike, contract_size=100):
    return 2 * (prem + vol * max(2 * stock_price - strike, stock_price)) * contract_size

def calc_put_margin(prem, vol, stock_price, strike, contract_size=100):
    return min(2 * (prem + vol * max(2 * strike - stock_price, strike)) * contract_size, strike* contract_size)
