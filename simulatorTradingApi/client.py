from simulatorTradingApi.userAccount.Account import Account
from simulatorTradingApi.trader.Trader import Trader, TRANSACTION_TYPE, DURATION

import pprint

pp = pprint.PrettyPrinter(indent=4)

account = Account("wuhui8013ee", "google@88", True)

trader = Trader(account)

trader.market_trade("ICLN", TRANSACTION_TYPE['BUY'], duration=DURATION['GOOD_TILL_CANCELLED'], quantity=20)



account.closeSession()

# trader = Trader(account)
# trader.trade("AAPL", "BUY", 32, None)

# account.closeSession()
# while 1:
#     sleep(20)
#     account.closeSession()
#     break
