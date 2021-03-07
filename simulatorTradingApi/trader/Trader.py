from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from ..utils.Exceptions import InvalidPriceType, InvalidDuration, InvalidLimitPrice, InvalidStopPrice

from simulatorTradingApi.utils.NumbersUtil import extract_number_from_sentence
from simulatorTradingApi.utils.StockUtils import get_stock_amount

import time
import logging

logging.basicConfig(level=logging.INFO)

DURATION = {
    "GOOD_TILL_CANCELLED": 'good_till_cancelled',
    "DAY_ORDER": "day_order"
}

PRICE_TYPE = {
    "MARKET": "market",
    "LIMIT": "limit",
    "STOP": "stop"
}

class Trader:
    def __init__(self, account):
        if not account.is_logged_in:
            raise Exception(
                "Account is not logged in. Please authenticate first!")
        else:
            self.account = account
            self.cash = account.get_portfolio()['cash']

    def __submit_order(self, client):
        previewOrder = client.find_element_by_id('previewButton')
        client.execute_script("arguments[0].click();", previewOrder)
        submitOrder = WebDriverWait(client, 10).until(
            EC.presence_of_element_located((By.ID, "submitOrder"))
        )
        client.execute_script("arguments[0].click();", submitOrder)

    def get_max_amount(self, symbol):
        try:
            client = HeadlessClient.get_instance()
            self.set_symbol(symbol)

            client.implicitly_wait(3)

            show_max_link = WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.ID, "showMaxLink"))
            )

            show_max_link.click()

            limitation_label = WebDriverWait(client, 10).until(
                EC.visibility_of_element_located((By.ID, "limitationLabel"))
            )

            max_amount = extract_number_from_sentence(
                limitation_label.get_attribute('innerText'))[0]

            return max_amount

        except Exception as e:
            logging.error("Failed to get max amount.", exc_info=True)

    def set_symbol(self, symbol):
        client = HeadlessClient.get_instance()
        symbol_input = WebDriverWait(client, 10).until(
            EC.presence_of_element_located((By.ID, "symbolTextbox"))
        )
        symbol_input.send_keys(symbol)
        symbol_input.send_keys(Keys.ENTER)

    def set_buy_input(self, price_type, quantity, duration=DURATION['GOOD_TILL_CANCELLED'],
                      send_confirmation=True, limit_price=None, stop_price=None):
        client = HeadlessClient.get_instance()

        # set transaction type to buy
        transaction_type_select = Select(
            client.find_element_by_id('transactionTypeDropDown'))
        transaction_type_select.select_by_value("1")

        self._set_common_input(quantity, duration, send_confirmation)
        self.set_price_type_input(price_type, limit_price, stop_price)

    def set_sell_input(self, price_type, quantity, duration=DURATION['GOOD_TILL_CANCELLED'],
                      send_confirmation=True, limit_price=None, stop_price=None, trailing_stop=False):
        client = HeadlessClient.get_instance()

        # set transaction type to sell
        transaction_type_select = Select(
            client.find_element_by_id('transactionTypeDropDown'))
        transaction_type_select.select_by_value("2")

        self._set_common_input(quantity, duration, send_confirmation)
        self.set_price_type_input(price_type, limit_price, stop_price)

        # if trailing_stop:
        #     trailing_stop_radio = client.find_element_by_id('tStopRadioButton')
        #     trailing_stop_radio.click()


    def set_price_type_input(self, price_type, limit_price=None, stop_price=None):
        client = HeadlessClient.get_instance()

        if price_type == PRICE_TYPE['MARKET']:
            marketSaleButton = client.find_element_by_id('marketPriceRadioButton')
            marketSaleButton.click()
        elif price_type == PRICE_TYPE['LIMIT']:
            limitSaleButton = client.find_element_by_id('limitRadioButton')
            limitSaleButton.click()

            # set limit price
            if limit_price is None:
                raise InvalidLimitPrice(limit_price)

            limitPriceBox = client.find_element_by_id('limitPriceTextBox')
            limitPriceBox.send_keys(str(limit_price))

        elif price_type == PRICE_TYPE['STOP']:
            stopSaleButton = client.find_element_by_id('stopRadioButton')
            stopSaleButton.click()

            if stop_price is None:
                raise InvalidStopPrice(stop_price)

            stopPriceBox = client.find_element_by_id('stopPriceTextBox')
            stopPriceBox.send_keys(str(stop_price))
        else:
            raise InvalidPriceType(price_type)

    def _set_common_input(self, quantity, duration=DURATION['GOOD_TILL_CANCELLED'], send_confirmation=True):
        client = HeadlessClient.get_instance()

        # Set duration
        durationSelect = Select(
            client.find_element_by_id('durationTypeDropDown'))
        if duration == DURATION['GOOD_TILL_CANCELLED']:
            durationSelect.select_by_value("2")
        elif duration == DURATION['DAY_ORDER']:
            durationSelect.select_by_value("1")
        else:
            raise InvalidDuration(duration)

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

    def buy(self, symbol, price_type, quantity, limit_price=None, stop_price=None, duration=DURATION['GOOD_TILL_CANCELLED'],
            send_confirmation=True):
        try:
            client = HeadlessClient.get_instance()
            client.get(
                "https://www.investopedia.com/simulator/trade/tradestock.aspx")

            max_buy_amount = self.get_max_amount(symbol)
            if quantity > max_buy_amount:
                logging.info(
                    f"Cannot place an order with quantity higher than {max_buy_amount}")
            else:
                self.set_buy_input(price_type, quantity, duration, send_confirmation, limit_price, stop_price)
                self.__submit_order(client)
        except Exception as e:
            self.account.close_session()
            logging.error("Failed to buy.", exc_info=True)
            raise e
        
    def sell(self, symbol, price_type, quantity, limit_price=None, stop_price=None, trailing_stop=False,
             duration=DURATION['GOOD_TILL_CANCELLED'], send_confirmation=True):
        try:
            client = HeadlessClient.get_instance()
            client.get(
                "https://www.investopedia.com/simulator/trade/tradestock.aspx")

            amount = get_stock_amount(self.account, symbol)
            if amount == 0:
                logging.info("You do not own this stock.")
                return
            elif quantity > amount:
                logging.info(f"You don't have {quantity} shares of {symbol}")
                return
            else:
                self.set_symbol(symbol)
                self.set_sell_input(price_type, quantity, duration, send_confirmation,
                                    limit_price, stop_price, trailing_stop)
                self.__submit_order(client)
        except Exception as e:
            logging.error("Failed to sell.", exc_info=True)
            self.account.close_session()
            raise e