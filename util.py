from datetime import datetime, timedelta
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