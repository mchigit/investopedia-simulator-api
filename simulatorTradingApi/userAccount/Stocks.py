from ..utils.NumbersUtil import extractNumberFromMoney, extractTodaysChange


class Stock:
    def __init__(self, symbol, name, qty, purchaseCost, currentPrice, todaysChange):
        self.symbol = symbol
        self.name = name
        self.qty = int(qty)
        self.purchaseCost = extractNumberFromMoney(purchaseCost)
        self.currentPrice = extractNumberFromMoney(currentPrice)
        self.todayChange = extractTodaysChange(todaysChange)
        self.purchaseCostTotal = round(self.qty * self.purchaseCost, 2)
        self.currentValue = round(self.qty * self.currentPrice, 2)
        self.profit = round(self.currentValue - self.purchaseCostTotal, 2)
        self.profitPercent = (self.profit - self.purchaseCostTotal) * 100

    def __str__(self):
        return (
            f"Symbol: {self.symbol}  |  "
            f"Name: {self.name}  |  "
            f"Quantity: {self.qty}  |  "
            f"Purchase Price: {self.purchaseCost} "
            f" |  Current Price: {self.currentPrice}  "
            f" |  Total Value: {self.currentValue}  |  "
            f"Total Profit: {self.profit}  |  Today's Change: {self.todayChange[0]}({self.todayChange[1]}%)"
        )
