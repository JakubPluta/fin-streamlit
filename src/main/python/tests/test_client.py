from client import AlphaVantageClient, Stock


def test_stock():
    stock = AlphaVantageClient()
    ic = stock.income_statement("FB")
    assert ic
