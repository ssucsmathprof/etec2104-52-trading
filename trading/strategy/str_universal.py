import requests
import json
from trading import models
from Strategy_Objects import OrderBook, Trader
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

TheOrderBook = OrderBook([])



def check_for_errors(json_response):
    '''
    Returns Error Request if Error in json response, and None otherwise.
    '''
    if not isinstance(json_response, dict):
        return None
    details = json_response.get("detail")
    if details is None:
        return None
    return RequestError(details.status_code, json_response["detail"])


def place_order(trader, symbol, price, side, quantity):
    '''
    Send a place order to the server.
    '''
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

    placed_order = Order.from_dict(response_dict)
    TheOrderBook.append(placed_order)
    return placed_order

def get_recent_orders(trader):
    '''
    Gets all recent orders a trader has placed.
    '''
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
    '''
    Returns the recent trades that a given trader has placed.
    '''
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
        trade_object = Order.from_dict(trade_dict)
        all_trades.append(trade_object)

    return all_trades

def get_orderbook_orders():
    '''
    Gets a list of all orders that any strategy has placed.
    '''
    return TheOrderBook.get_all_orders()

def can_buy(trader):
    ...
    #you got coin?

def get_best_rate(market_symbol):
    '''
    Gets the best rate for a given market symbol.
    '''
    market_picture = TheOrderBook.get_all_orders()
    best_rate = 0
    for order in market_picture:
        if order.symbol == market_symbol and order.price > best_rate:
            best_rate = order.price

    return best_rate

trader = models.Trader.objects.get(username="teama")
print(get_recent_orders(trader))
#place_order()