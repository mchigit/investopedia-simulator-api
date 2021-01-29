from simulatorTradingApi.userAccount.Account import Account
from simulatorTradingApi.trader.Trader import Trader, TRANSACTION_TYPE, DURATION

import pprint
from time import sleep

pp = pprint.PrettyPrinter(indent=4)

account = Account("wuhui8013ee", "google@88", True)

trader = Trader(account)

#trader.market_trade("AMC", TRANSACTION_TYPE['BUY'], duration=DURATION['GOOD_TILL_CANCELLED'], quantity=100)
sleep(5)

trader.stop_trade("GME", TRANSACTION_TYPE['BUY'], 30, 300)

sleep(5)



account.close_session()

# trader = Trader(account)
# trader.trade("AAPL", "BUY", 32, None)

# account.close_session()
# while 1:
#     sleep(20)
#     account.close_session()
#     break
