from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from simulatorTradingApi.utils.TraderUtil import extractNumberFromSentence

# class element_is_not_hidden(object):
#     """An expectation for checking that an element is not hidden.
#
#     locator - used to find the element
#     returns the WebElement once it has the particular css class
#     """
#     def __init__(self, locator):
#         self.locator = locator
#
#     def __call__(self, driver):
#         element = driver.find_element(*self.locator)
#         if element.get_attribute

class Trader:

    def __init__(self, account):
        if not account.isLoggedIn:
            raise Exception("Account is not logged in. Please authenticate first!")
        else:
            self.user = account
            self.cash = account.user.cash

    def trade(self, symbol, tradeType, quantity, duration, sendConfirmation = True):
        client = HeadlessClient.getInstance()
        client.get("https://www.investopedia.com/simulator/trade/tradestock.aspx")

        symbolInput  = WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.ID, "symbolTextbox"))
        )
        symbolInput.send_keys(symbol)
        symbolInput.send_keys(Keys.ENTER)

        # limitationLable = WebDriverWait(client, 10).until(
        #         EC.presence_of_element_located((By.ID, "symbolTextbox"))
        # )




        # maximumNumberOfShares = extractNumberFromSentence(client.find_element_by_id('limitationLabel').get_attribute("innerText"))

        # print(maximumNumberOfShares)
