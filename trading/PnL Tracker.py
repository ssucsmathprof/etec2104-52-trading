from pylogger import get_logger
from views import get_trader
from tradebot import RequestError
import requests
import json

logger = get_logger()

BASE_URL = "http://127.0.0.1:8000/api"

## Get all orders from a Trader
logger = get_logger()
def check_response_for_errors(response):
    ## TODO Implement This
    # I think i did it right but check me on it
    '''
    Returns Error Request if Error in json response, and None otherwise.
    '''
    if not isinstance(response, dict):
        return None
    details = response.get("detail")
    if details is None:
        return None

    error = RequestError(details.status_code, response["detail"])
    logger.error(f"An error was give, {error}")
    return error

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
            realized_gains_dict[trade["symbol"]] = []

    bundle_tuple = (trade["quantity"], trade["price"])
    realized_gains_dict[trade["symbol"]].append(bundle_tuple)

    realized_purchase_dict = {}
    for symbol in realized_gains_dict:

        totals_spent = 0
        totals_qty = 0
        for bundle in trade["symbol"]:
            totals_spent += bundle[1]
            totals_qty += bundle[0]
        realized_purchase_dict[symbol] = totals_spent / totals_qty

    actual_realized_gains = {}
    for order in order_list:
        if order["symbol"] in actual_realized_gains:
            realized_gains_dict[order["symbol"]] = order["quantity"] * order["price"] - actual_realized_gains[
                order["symbol"]]

def check_unrealized_gains():
    ...
    ## What I need is a dictionary that has the key being the symbol and the qty the average price I spent for each item
    ## THen I compare that against a market screenshot

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



