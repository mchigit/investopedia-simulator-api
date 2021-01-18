from simulatorTradingApi.userAccount.Account import Account

import pprint

pp = pprint.PrettyPrinter(indent=4)

account = Account("wuhui8013ee", "google@88")

account.authenticate()

pp.pprint(account.getAccountStatus())
pp.pprint(account.getHoldings())

account.closeSession()

# trader = Trader(account)
# trader.trade("AAPL", "BUY", 32, None)

# account.closeSession()
# while 1:
#     sleep(20)
#     account.closeSession()
#     break
