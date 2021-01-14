from simulatorTradingApi.config import config
from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from simulatorTradingApi.Account import Account


account = Account("wuhui8013ee", "google@88")

account.authenticate()

account.closeSession()
