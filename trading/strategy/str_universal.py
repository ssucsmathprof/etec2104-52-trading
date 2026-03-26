import requests
import json
from trading import models
from tradebot import MarketReport, Order, RequestError, Symbol

#SYMBOLS = ['BEAR', 'FROG', 'LZRD']
#SIDES = ("BUY", "SELL")

BASE_URL = "http://127.0.0.1:8000/"
MARKET_URL = BASE_URL + "api/market/"
PLACE_ORDER_URL = BASE_URL + "api/orders"
RECENT_ORDER_URL = BASE_URL + "api/orders/open"
RECENT_TRADE_URL = BASE_URL + "api/trades/recent"

SIDE_BUY = "BUY"
SIDE_SELL = "SELL"


# class ErrorCode:
#     def __init__(self, status_code, details):
#         details = details
#         code = status_code
#
#
# class Order():
#     def __init__(self, order_dict):
#         self.id = order_dict["id"]
#         self.trader = order_dict["trader"]
#         self.symbol = order_dict["symbol"]
#         self.side = order_dict["side"]
#         self.quantity = int(order_dict["quantity"])
#         self.remaining = int(order_dict["remaining"])
#         self.price = float(order_dict["price"])
#         self.created_at = order_dict["created_at"]
#
# class Trade():
#     def __init__(self, trade_dict):
#         self.id = int(trade_dict["id"])
#         self.symbol = trade_dict["symbol"]
#         self.buyer = trade_dict["buyer"]
#         self.seller = trade_dict["seller"]
#         self.quantity = int(trade_dict["quantity"])
#         self.price = float(trade_dict["price"])
#         self.created_at = trade_dict["created_at"]
#
# class Trader():
#
#     def __init__(self, trader_dict):
#         self.id = (int)trader_dict["id"]
#         self.username = trader_dict["username"]
#         self.password = trader_dict["password"]

# def dict_to_order(order_dict):
#     return models.Order(
#         id=int(order_dict["id"]),
#         trader=order_dict["trader"],
#         symbol=order_dict["symbol"],
#         side=order_dict["side"],
#         quantity=int(order_dict["quantity"]),
#         remaining=int(order_dict["remaining"]),
#         price=float(order_dict["price"]),
#         created_at=order_dict["created_at"],
#         #price=decimal.Decimal(order_dict["price"]),
#         #created_at=datetime.datetime.fromisoformat(order_dict["created_at"]),
#     )

# def dict_to_trade(trade_dict):
#     return models.Trade(
#         id=int(trade_dict["id"]),
#         symbol = trade_dict["symbol"],
#         buyer = trade_dict["buyer"],
#         seller = trade_dict["seller"],
#         quantity = int(trade_dict["quantity"]),
#         price=float(trade_dict["price"]),
#         created_at=trade_dict["created_at"],
#     )


def check_for_errors(json_response):
    if not isinstance(json_response, dict):
        return None
    if json_response.get("detail") is None:
        return None
    return ErrorCode(json_response["status code"], json_response["detail"])

def place_order(trader, symbol, price, side, quantity):
    order_data = {
            "symbol": symbol,
            "price": price,
            "side": side,
            "quantity": quantity
        }
    auth = (trader.username, trader.password)

    server_response = requests.post(
        PLACE_ORDER_URL,
        json=order_data,
        auth=auth)
    response_dict = server_response.json()

    error_check = check_for_errors(response_dict)
    if not error_check is None:
        return error_check

    order = dict_to_order(response_dict)
    return order

def get_recent_orders(trader):
    response = requests.get(
        url=RECENT_ORDER_URL,
        auth=(trader.username, trader.password),
    )
    all_orders: list[models.Order] = []

    list_orders_dict = response.json()  # just raw list[dict[]]

    error_check = check_for_errors(list_orders_dict)
    if not error_check is None:
        return error_check

    for order_dict in list_orders_dict:
        order_object = dict_to_order(order_dict)
        all_orders.append(order_object)

    return all_orders


def get_recent_trades(trader):
    response = requests.get(
        url=RECENT_TRADE_URL,
        auth=(trader.username, trader.password),
    )
    all_trades: list[models.Trade] = []

    list_trade_dict = response.json()  # just raw list[dict[]]

    error_check = check_for_errors(list_trade_dict)
    if not error_check is None:
        return error_check

    for trade_dict in list_trade_dict:
        trade_object = dict_to_trade(trade_dict)
        all_trades.append(trade_object)

    return all_trades

def get_market_picture():
    #kylie will work on this
    #get market snapshot as a list of orders
    #needs createdAt
    pass

def can_buy(trader):
    ...
    #you got coin?

def get_best_rate(market_symbol):
    market_picture = get_market_picture()
    best_rate = 0
    for order in market_picture:
        if order.symbol == market_symbol and order.price > best_rate:
            best_rate = order.price

    return best_rate

trader = models.Trader.objects.get(username="teama")
get_recent_orders(trader)
#place_order()