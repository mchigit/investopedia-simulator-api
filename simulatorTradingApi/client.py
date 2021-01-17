from simulatorTradingApi.config import config
from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from simulatorTradingApi.Account import Account
from simulatorTradingApi.Trader import Trader

from time import sleep

account = Account("wuhui8013ee", "google@88")

account.authenticate()

# trader = Trader(account)
# trader.trade("AAPL", "BUY", 32, None)

# account.closeSession()
while 1:
    sleep(20)
    account.closeSession()
    break
