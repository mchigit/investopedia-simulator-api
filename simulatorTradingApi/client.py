from simulatorTradingApi.userAccount.Account import Account

import pprint

pp = pprint.PrettyPrinter(indent=4)

account = Account("wuhui8013ee", "google@88")

holdings = account.user.getHoldings()

for holding in holdings:
    print(holding)

account.closeSession()

# trader = Trader(account)
# trader.trade("AAPL", "BUY", 32, None)

# account.closeSession()
# while 1:
#     sleep(20)
#     account.closeSession()
#     break
