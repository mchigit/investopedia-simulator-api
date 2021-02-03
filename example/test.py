from simulatorTradingApi.userAccount.Account import Account
from simulatorTradingApi.trader.Trader import Trader, TRANSACTION_TYPE, DURATION

account = Account("wuhui8013ee", "google@88", True)

print(account.get_portfolio())