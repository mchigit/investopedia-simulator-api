from ..seleniumUtil.HeadlessClient import HeadlessClient
from ..utils.NumbersUtil import extract_number_from_money, extract_percentage
from .Holdings import Holdings

import logging

logging.basicConfig(level=logging.INFO)


class UserPortfolio:
    account_value_usd = 0
    buying_power = 0
    cash = 0
    annual_return = 0
    __holdings = None

    def __init__(self):
        self.retrieve_portfolio()

    def retrieve_portfolio(self):
        try:
            client = HeadlessClient.get_instance()
            client.get("https://www.investopedia.com/simulator/portfolio/")
            info = client.find_elements_by_class_name("infobar-title")

            if len(info) < 4:
                print("Failed to retrieve user portfolio")
                return

            account_value_usd = (
                info[0]
                .find_element_by_tag_name("p")
                .find_element_by_css_selector(":nth-child(2)")
                .get_attribute("innerText")
            )

            buying_power = (
                info[1]
                .find_element_by_tag_name("p")
                .find_element_by_css_selector(":nth-child(2)")
                .get_attribute("innerText")
            )

            cash = (
                info[2]
                .find_element_by_tag_name("p")
                .find_element_by_css_selector(":nth-child(2)")
                .get_attribute("innerText")
            )

            annual_return = (
                info[3]
                .find_element_by_tag_name("p")
                .find_element_by_css_selector(":nth-child(2)")
                .get_attribute("innerText")
            )

            self.account_value_usd = extract_number_from_money(account_value_usd)
            self.buying_power = extract_number_from_money(buying_power)
            self.cash = extract_number_from_money(cash)
            self.annual_return = extract_percentage(annual_return)
            self.__holdings = Holdings()
            
        except Exception as e:
            logging.error("Failed to retrieve user portfolio.", exc_info=True)

    def get_portfolio(self):
        return {
            "account_value_usd": self.account_value_usd,
            "buying_power": self.buying_power,
            "cash": self.cash,
            "annual_return": self.annual_return,
        }

    def refresh(self):
        self.retrieve_portfolio()

    def get_holdings(self):
        return self.__holdings.get_holdings()
