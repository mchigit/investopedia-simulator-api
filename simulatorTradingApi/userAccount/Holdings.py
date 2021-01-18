from ..seleniumUtil.HeadlessClient import HeadlessClient
from .Stocks import Stock


def extractStockInfo(stockTableElement):
    stockBody = stockTableElement.find_elements_by_tag_name("tbody")[0]
    stockTotal = stockTableElement.find_elements_by_tag_name("tbody")[1]

    stocks = stockBody.find_elements_by_css_selector("tr:nth-child(odd)")
    stockObjects = []

    for stock in stocks:
        symbolElem = stock.find_element_by_css_selector(
            "td:nth-child(3)"
        ).find_element_by_css_selector("a:nth-child(2)")
        symbol = symbolElem.get_attribute("innerText")
        name = stock.find_element_by_css_selector("td:nth-child(4)").get_attribute(
            "innerText"
        )
        qty = stock.find_element_by_css_selector("td:nth-child(5)").get_attribute(
            "innerText"
        )
        purchasePrice = stock.find_element_by_css_selector(
            "td:nth-child(6)"
        ).get_attribute("innerText")
        currentPrice = stock.find_element_by_css_selector(
            "td:nth-child(7)"
        ).get_attribute("innerText")

        stockObject = Stock(symbol, name, qty, purchasePrice, currentPrice)
        stockObjects.append(stockObject)

    return stockObjects


class Holdings:
    holdings = []

    def __init__(self):
        client = HeadlessClient.getInstance()
        client.get("https://www.investopedia.com/simulator/portfolio/")
        stockTable = client.find_element_by_id("stock-portfolio-table")
        self.holdings = extractStockInfo(stockTable)

    def getHoldings(self):
        return self.holdings
