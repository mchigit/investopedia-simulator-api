class InvalidPriceType(Exception):
    """
    Exception raised for invalid price types
    Accepted price type:
        PRICE_TYPE = {
            "MARKET": "market",
            "LIMIT": "limit",
            "STOP": "stop"
        }

    Attributes:
         invalid_price_type -- input price type that caused the error
         msg -- customized error message
    """

    def __init__(self, invalid_price_type, msg=None):
        self.invalid_price_type = invalid_price_type
        self.msg = msg if msg is not None else "Invalid price type. Accepted types: " \
                                               "PRICE_TYPE[\"MARKET\"]," \
                                               " PRICE_TYPE[\"LIMIT\"]," \
                                               " PRICE_TYPE[\"STOP\"]"
        super().__init__(self.msg)

    def __str__(self):
        return f'Invalid price type: {self.invalid_price_type}. \n {self.msg}'

class InvalidDuration(Exception):
    """
    Exception raised for invalid durations
    Accepted duration type:
            DURATION = {
                "GOOD_TILL_CANCELLED": 'good_till_cancelled',
                "DAY_ORDER": "day_order"
            }

    Attributes:
         invalid_duration -- input duration that caused the error
         msg -- customized error message
    """

    def __init__(self, invalid_duration, msg=None):
        self.invalid_duration = invalid_duration
        self.msg = msg if msg is not None else "Invalid duration type. Accepted types: " \
                                               "DURATION[\"GOOD_TILL_CANCELLED\"]," \
                                               " DURATION[\"DAY_ORDER\"]"
        super().__init__(self.msg)

    def __str__(self):
        return f'Invalid duration type: {self.invalid_duration}. \n {self.msg}'

class InvalidLimitPrice(Exception):
    """
    Exception raised for limit order caused by invalid limit price

    Attributes:
         invalid_limit_price -- input limit price that caused the error
         msg -- customized error message
    """

    def __init__(self, invalid_limit_price, msg=None):
        self.invalid_limit_price = invalid_limit_price
        self.msg = msg if msg is not None else f"Limit price is invalid: {self.invalid_limit_price}"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg

class InvalidStopPrice(Exception):
    """
    Exception raised for stop order caused by invalid stop price

    Attributes:
         invalid_stop_price -- input limit price that caused the error
         msg -- customized error message
    """

    def __init__(self, invalid_stop_price, msg=None):
        self.invalid_stop_price = invalid_stop_price
        self.msg = msg if msg is not None else f"Stop price is invalid: {self.invalid_stop_price}"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg
