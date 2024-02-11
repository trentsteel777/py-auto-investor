from datetime import datetime
from enum import Enum
import re

class OptionType(Enum):
    CALL = 'CALL'
    PUT = 'PUT'

def generate_contract_symbol(symbol, expiry, option_type, strike):
    # Format expiry date
    expiry_str = expiry.strftime('%y%m%d')

    # Format strike with padding
    strike_str = '{:.0f}'.format(strike * 1000)
    strike_with_padding = strike_str.zfill(8)

    # Get option type character
    option_type_char = option_type.value[0].upper()

    # Concatenate components
    return symbol + expiry_str + option_type_char + strike_with_padding

# Example usage
symbol = 'AAPL'
expiry = datetime.strptime('2024-02-20', '%Y-%m-%d').date()
option_type = OptionType.PUT
strike = 100.0

contract_symbol = generate_contract_symbol(symbol, expiry, option_type, strike)
print("Contract Symbol:", contract_symbol)


    