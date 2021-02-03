# Investopedia Trading Simulator API

A library that can be used to interact with Investopedia's simulator trading game. The library uses selenium for scraping information and making trades. 


# Features
1. Login and retrieving account information (Cash, buying power)
2. Retrieve account holdings
3. Retrieve account transaction history (coming)
4. Making trades (Market, limit, stop limit)

# Quick-start

## Requirement
- python > 3.7
- virtualenv
- chromedriver corresponding to your own chrome version
<br/>

## Install
Navigate to project root and run the following command:
```bash
# Using a virtualenv is recommended but not required
python3 -m venv venv
source venv/bin/activate

pip install simulatorTradingApi
```

The library uses Selenium to launch a headless browser for scraping information and making trades. Therefore, you need to download a chromedriver that matches your Chrome version. 

By default, the library will try to find the driver at `$HOME/driver/chromedriver`. 

You can also set the environment variable `CHROMEDRIVER_PATH` if your chromedriver is stored somewhere else.  

<br/>

# Basic Usage

<br/>

## Account Related
```python
# Connecting your account
from simulatorTradingApi.userAccount.Account import Account

account = Account(username, password, auto_refresh=True)

# Retrieving portfolio
"""
Example Return:
{
    "account_value_usd": 1000,
    "buying_power": 3000,
    "cash": 300,
    "annual_return": 60
}

annual_return is a number indicating percentage return.
"""
account.get_portfolio()

# Get holdings (Currently only stocks)
"""
Returns a list of Stock objects

Example Return:
[Stock 1, Stock 2, Stock 3]
"""
stocks = account.get_holdings()
for stock in stocks:
    print(stocks)
```

<br />

> It's important to remember to close the session once you are done with operations. If you don't close the session, the headless browser will remain open and the thread that is responsible for refreshing will keep executing.

<br />

## Trading
