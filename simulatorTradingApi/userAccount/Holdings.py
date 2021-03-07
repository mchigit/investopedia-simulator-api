from ..seleniumUtil.HeadlessClient import HeadlessClient
from .Stocks import Stock

import logging
logging.basicConfig(level=logging.INFO)


def extract_stock_info(stock_table_element):
    try:
        stock_body = stock_table_element.find_elements_by_tag_name("tbody")[0]
        stock_total = stock_table_element.find_elements_by_tag_name("tbody")[1]

        stocks = stock_body.find_elements_by_css_selector("tr:nth-child(odd)")
        stock_objects = []

        for stock in stocks:
            symbol_elem = stock.find_element_by_css_selector(
                "td:nth-child(3)"
            ).find_element_by_css_selector("a:nth-child(2)")

            symbol = symbol_elem.get_attribute("innerText")

            name = stock.find_element_by_css_selector("td:nth-child(4)").get_attribute(
                "innerText"
            )

            qty = stock.find_element_by_css_selector("td:nth-child(5)").get_attribute(
                "innerText"
            )

            purchase_price = stock.find_element_by_css_selector(
                "td:nth-child(6)"
            ).get_attribute("innerText")

            current_price = stock.find_element_by_css_selector(
                "td:nth-child(7)"
            ).get_attribute("innerText")

            todays_change = stock.find_element_by_css_selector(
                "td:nth-child(9)"
            ).get_attribute("innerText")

            stock_object = Stock(
                symbol, name, qty, purchase_price, current_price, todays_change
            )

            stock_objects.append(stock_object)

        return stock_objects
    except Exception as e:
        logging.error("Failed to retrieve holdings.", exc_info=True)
class Holdings:

    holdings = []

    def __init__(self):
        self.refresh()

    def get_holdings(self):
        return self.holdings

    def refresh(self):
        client = HeadlessClient.get_instance()
        client.get("https://www.investopedia.com/simulator/portfolio/")
        stock_table = client.find_element_by_id("stock-portfolio-table")
        self.holdings = extract_stock_info(stock_table)
    
        