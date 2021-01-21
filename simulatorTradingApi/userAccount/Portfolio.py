from ..seleniumUtil.HeadlessClient import HeadlessClient
from ..utils.NumbersUtil import extractNumberFromMoney, extractPercentage
from .Holdings import Holdings

import logging

logging.basicConfig(level=logging.INFO)


class UserPortfolio:
    accountValueUSD = 0
    buyingPower = 0
    cash = 0
    annualReturn = 0
    holdings = None

    def __init__(self):
        self.retrievePortfolio()

    def retrievePortfolio(self):
        try:
            client = HeadlessClient.getInstance()
            client.get("https://www.investopedia.com/simulator/portfolio/")
            info = client.find_elements_by_class_name("infobar-title")

            if len(info) < 4:
                print("Failed to retrieve user portfolio")
                return

            accountValueUSD = (
                info[0]
                .find_element_by_tag_name("p")
                .find_element_by_css_selector(":nth-child(2)")
                .get_attribute("innerText")
            )

            buyingPower = (
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

            annualReturn = (
                info[3]
                .find_element_by_tag_name("p")
                .find_element_by_css_selector(":nth-child(2)")
                .get_attribute("innerText")
            )

            self.accountValueUSD = extractNumberFromMoney(accountValueUSD)
            self.buyingPower = extractNumberFromMoney(buyingPower)
            self.cash = extractNumberFromMoney(cash)
            self.annualReturn = extractPercentage(annualReturn)
            self.holdings = Holdings()
        except Exception as e:
            logging.error("Failed to retrieve user portfolio.", exc_info=True)

    def getPortfolio(self):
        return {
            "accountValueUSD": self.accountValueUSD,
            "buyingPower": self.buyingPower,
            "cash": self.cash,
            "annualReturn": self.annualReturn,
        }

    def refresh(self):
        self.retrievePortfolio()

    def getHoldings(self):
        return self.holdings.getHoldings()
