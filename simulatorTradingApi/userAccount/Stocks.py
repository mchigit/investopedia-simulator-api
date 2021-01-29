from ..utils.NumbersUtil import extract_number_from_money, extract_todays_change


class Stock:
    def __init__(self, symbol, name, qty, purchase_cost, current_price, todays_change):
        self.symbol = symbol
        self.name = name
        self.qty = int(qty)
        self.purchase_cost = extract_number_from_money(purchase_cost)
        self.current_price = extract_number_from_money(current_price)
        self.today_change = extract_todays_change(todays_change)
        self.total_purchase_cost = round(self.qty * self.purchase_cost, 2)
        self.current_value = round(self.qty * self.current_price, 2)
        self.profit = round(self.current_value - self.total_purchase_cost, 2)
        self.profit_percent = (self.profit - self.total_purchase_cost) * 100

    def __str__(self):
        return (
            f"Symbol: {self.symbol}  |  "
            f"Name: {self.name}  |  "
            f"Quantity: {self.qty}  |  "
            f"Purchase Price: {self.purchase_cost} "
            f" |  Current Price: {self.current_price}  "
            f" |  Total Value: {self.current_value}  |  "
            f"Total Profit: {self.profit}  |  Today's Change: {self.today_change[0]}({self.today_change[1]}%)"
        )
