from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from simulatorTradingApi.utils.NumbersUtil import extract_number_from_sentence
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


def get_max_amount(symbol):
    try:
        client = HeadlessClient.get_instance()
        symbol_input = WebDriverWait(client, 10).until(
            EC.presence_of_element_located((By.ID, "symbolTextbox"))
        )
        symbol_input.send_keys(symbol)
        symbol_input.send_keys(Keys.ENTER)
        
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


class Trader:
    def __init__(self, account):
        if not account.is_logged_in:
            raise Exception(
                "Account is not logged in. Please authenticate first!")
        else:
            self.user = account
            self.cash = account.get_portfolio()['cash']

    def __set_market_trade_input(self, transcation_type, quantity, duration, send_confirmation):
        client = HeadlessClient.get_instance()

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

    def __submit_order(self, client):
        previewOrder = client.find_element_by_id('previewButton')
        client.execute_script("arguments[0].click();", previewOrder)
        submitOrder = WebDriverWait(client, 10).until(
            EC.presence_of_element_located((By.ID, "submitOrder"))
        )
        client.execute_script("arguments[0].click();", submitOrder)
    
    def market_trade(self, symbol, transcation_type, quantity, duration=DURATION['GOOD_TILL_CANCELLED'], send_confirmation=True):
        try:
            client = HeadlessClient.get_instance()
            client.get(
                "https://www.investopedia.com/simulator/trade/tradestock.aspx")

            max_buy_amount = get_max_amount(symbol)

            if quantity > max_buy_amount:
                logging.info(
                    f"Cannot place an order with quantity higher than {max_buy_amount}")
            else:
                self.__set_market_trade_input(
                    transcation_type, quantity, duration, send_confirmation)
                
                self.__submit_order(client)
                
                successMsg = f"Placed an order of {quantity} shares for {symbol}."
                logging.info(successMsg)

        except Exception as e:
            logging.error("Failed to place trade.", exc_info=True)

    def limit_trade(self, symbol, transcation_type, quantity, limit_price, duration=DURATION['GOOD_TILL_CANCELLED'], send_confirmation=True):
        try:
            client = HeadlessClient.get_instance()
            client.get(
                "https://www.investopedia.com/simulator/trade/tradestock.aspx")
            
            max_buy_amount = get_max_amount(symbol)
            
            if quantity > max_buy_amount:
                logging.info(
                    f"Cannot place an order with quantity higher than {max_buy_amount}")
            else:
                self.__set_market_trade_input(
                    transcation_type, quantity, duration, send_confirmation)
                
                limitSaleButton = client.find_element_by_id('limitRadioButton')
                limitSaleButton.click()
                
                limitPriceBox = client.find_element_by_id('limitPriceTextBox')
                limitPriceBox.send_keys(str(limit_price))
                
                self.__submit_order(client)
                
        except Exception as e:
            logging.error("Failed to place trade.", exc_info=True)
    
    
    def stop_trade(self, symbol, transcation_type, quantity, stop_price, duration=DURATION['GOOD_TILL_CANCELLED'], send_confirmation=True):
        try:
            client = HeadlessClient.get_instance()
            client.get(
                "https://www.investopedia.com/simulator/trade/tradestock.aspx")
            
            max_buy_amount = get_max_amount(symbol)
            
            if quantity > max_buy_amount:
                logging.info(
                    f"Cannot place an order with quantity higher than {max_buy_amount}")
            else:
                self.__set_market_trade_input(
                    transcation_type, quantity, duration, send_confirmation)
                
                limitSaleButton = client.find_element_by_id('stopRadioButton')
                limitSaleButton.click()
                
                limitPriceBox = client.find_element_by_id('stopPriceTextBox')
                limitPriceBox.send_keys(str(stop_price))
                
                self.__submit_order(client)
                
        except Exception as e:
            logging.error("Failed to place trade.", exc_info=True)