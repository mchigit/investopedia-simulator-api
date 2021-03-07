def get_stock_amount(account, symbol):
    holdings = account.get_holdings()
    for stock in holdings:
        if stock.symbol == symbol:
            return stock.qty

    return 0
