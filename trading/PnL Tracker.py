from pylogger import get_logger
from views import get_trader
import requests
logger = get_logger()

BASE_URL = "http://127.0.0.1:8000/api"

## Get all orders from a Trader

def check_response_for_errors(response):
    ## TODO Implement This
    pass

def check_realized_gains(trader_object):
    order_list = requests.get(
        BASE_URL + "/orders/open",
        auth=(trader_object.username, trader_object.password)
    )

    trade_list = requests.get(
        BASE_URL + "/trades/recent",
        auth=(trader_object.username, trader_object.password)
    )

    check_response_for_errors(order_list)
    check_response_for_errors(trade_list)



    realized_gains_dict = {}

    for trade in trade_list:
        if trade["symbol"] not in realized_gains_dict:
            realized_gains_dict[trade["symbol"]] = 0

        realized_gains_dict[trade["symbol"]] += trade["quantity"] * trade["price"]

    for order in order_list:
        if order["symbol"] in realized_gains_dict:
            realized_gains_dict[order["symbol"]] -= order["quantity"] * order["price"]




def check_unrealized_gains():
    pass

def check_cash_discrepancy(trader_object):
    trader_exchange = get_trader(trader_object.username)

    response = requests.get(
        BASE_URL + "/me",
        auth=(trader_object.username, trader_object.password)
    )
    check_response_for_errors(response)


    if response["cash"] == trader_object.cash:
        logger.info("The exchange trader's cash and trader object cash are in sync")
    else:
        logger.warning(f"Descrepency detected between Exchange Trader's Cash{response["cash"]} and Object Trader's Cash{trader_object.cash}")



