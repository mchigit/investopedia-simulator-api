from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from simulatorTradingApi.utils.NumbersUtil import extractNumberFromSentence
from simulatorTradingApi.userAccount.Account import Account

import time
import logging
logging.basicConfig(level=logging.INFO)

TRANSACTION_TYPE = {
    'BUY': 'buy',
    'SELL': 'sell',
    'SELL_SHORT': 'sell_short',
    'BUY_TO_COVER': 'buy_to_cover'
}

PRICE_TYPE = {
    'MARKET': 'market',
    'LIMIT': 'limit',
    'STOP': 'stop'
}

DURATION = {
    "GOOD_TILL_CANCELLED": 'good_till_cancelled',
    "DAY_ORDER": "day_order"
}


class Trader:
    def __init__(self, account):
        if not account.isLoggedIn:
            raise Exception(
                "Account is not logged in. Please authenticate first!")
        else:
            self.user = account
            self.cash = account.getPortfolio()['cash']

    def __set_market_trade_input(self, transcation_type, quantity, duration, send_confirmation):
        client = HeadlessClient.getInstance()

        # set market trade radio
        market_trade_radio = client.find_element_by_id(
            'marketPriceRadioButton')
        market_trade_radio.click()

        # Set transaction type dropdown
        transactionTypeSelect = Select(
            client.find_element_by_id('transactionTypeDropDown'))
        if transcation_type == TRANSACTION_TYPE['BUY']:
            transactionTypeSelect.select_by_value("1")
        elif transcation_type == TRANSACTION_TYPE['SELL']:
            transactionTypeSelect.select_by_value("2")
        elif transcation_type == TRANSACTION_TYPE['SELL_SHORT']:
            transactionTypeSelect.select_by_value("3")
        elif transcation_type == TRANSACTION_TYPE['BUY_TO_COVER']:
            transactionTypeSelect.select_by_value("4")
        else:
            raise Exception(
                f"Transaction type is not supported: {transcation_type}")

        # Set duration
        durationSelect = Select(
            client.find_element_by_id('durationTypeDropDown'))
        if duration == DURATION['GOOD_TILL_CANCELLED']:
            durationSelect.select_by_value("2")
        elif duration == DURATION['DAY_ORDER']:
            durationSelect.select_by_value("1")
        else:
            raise Exception(f"Duration type is not supported: {duration}")

        # Set confirmation
        confirmationCheckBox = client.find_element_by_id(
            'sendConfirmationEmailCheckBox')
        if not send_confirmation:
            if confirmationCheckBox.get_attribute('checked'):
                confirmationCheckBox.click()
        else:
            if not confirmationCheckBox.get_attribute('checked'):
                confirmationCheckBox.click()

        # set quantity
        client.find_element_by_id('quantityTextbox').send_keys(str(quantity))

    def market_trade(self, symbol, transcation_type, quantity, duration=DURATION['GOOD_TILL_CANCELLED'], sendConfirmation=True):
        try:
            client = HeadlessClient.getInstance()
            client.get(
                "https://www.investopedia.com/simulator/trade/tradestock.aspx")

            symbolInput = WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.ID, "symbolTextbox"))
            )
            symbolInput.send_keys(symbol)
            symbolInput.send_keys(Keys.ENTER)

            showMaxLink = WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.ID, "showMaxLink"))
            )

            showMaxLink.click()

            limitationLable = WebDriverWait(client, 10).until(
                EC.visibility_of_element_located((By.ID, "limitationLabel"))
            )

            maxBuyAmount = extractNumberFromSentence(
                limitationLable.get_attribute('innerText'))[0]

            if quantity > maxBuyAmount:
                logging.info(
                    f"Cannot place an order with quantity higher than {maxBuyAmount}")
            else:
                self.__set_market_trade_input(
                    transcation_type, quantity, duration, False)
                previewOrder = client.find_element_by_id('previewButton')
                client.execute_script("arguments[0].click();", previewOrder)
                submitOrder = WebDriverWait(client, 10).until(
                    EC.presence_of_element_located((By.ID, "submitOrder"))
                )
                client.execute_script("arguments[0].click();", submitOrder)
                successMsg = f"Placed an order of {quantity} shares for {symbol}."
                logging.info(successMsg)

        except Exception as e:
            Account.closeSession()
            logging.error("Failed to place trade.", exc_info=True)
