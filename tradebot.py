import decimal
from typing import NamedTuple
import datetime
import requests
import json
import sys
import csv
from pylogger import get_logger

logger = get_logger()

BASE_URL = "http://127.0.0.1:8000/api"

type TeamName = str


class RequestError(NamedTuple):
    status_code: int
    content: str

class Symbol(NamedTuple):
    """Representation of a single symbol as given by /api/market."""

    id: int
    code: str

    def from_dict(dict_symbol: dict):
        logger.debug(f"Creating Symbol object from JSON dictionary: {dict}")
        return Symbol(
            id=dict_symbol["id"],
            code=dict_symbol["code"],
        )

class MarketReport(NamedTuple):
    """Report on the current price of a single market/symbol as given by /api/market."""
    id: int
    symbol: Symbol
    last_price: decimal.Decimal
    updated_at: datetime.datetime

    def from_dict(dict_market: dict):
        logger.debug(f"Creating MarketReport object from JSON dictionary: {dict}")
        return MarketReport(
            id=dict_market["id"],
            symbol=Symbol.from_dict(dict_market["symbol"]),
            last_price=decimal.Decimal(dict_market["last_price"]),
            updated_at=datetime.datetime.fromisoformat(dict_market["updated_at"]),
        )

class Trade(NamedTuple):
    id: int
    symbol: str
    price: decimal.Decimal
    quantity: int
    buyer: str
    seller: str
    created_at: datetime.datetime

    def from_dict(dict_trade: dict):
        logger.debug(f"Creating Trade object from JSON dictionary: {dict}")
        return Trade(
            id=int(dict_trade["id"]),
            symbol=dict_trade["symbol"],
            price=decimal.Decimal(dict_trade["price"]),
            quantity=int(dict_trade["quantity"]),
            buyer=dict_trade["buyer"],
            seller=dict_trade["seller"],
            created_at=datetime.datetime.fromisoformat(dict_trade["created_at"]),
        )

class Order(NamedTuple):
    """Report on an order as given by /api/orders and /api/orders/open."""

    id: int
    trader: TeamName
    symbol: str
    side: str
    price: decimal.Decimal
    quantity: int
    remaining: int
    created_at: datetime.datetime

    def from_dict(dict_order: dict):
        logger.debug(f"Creating Order object from JSON dictionary: {dict}")
        return Order(
            id=int(dict_order["id"]),
            trader=dict_order["trader"],
            symbol=dict_order["symbol"],
            side=dict_order["side"],
            price=decimal.Decimal(dict_order["price"]),
            quantity=int(dict_order["quantity"]),
            remaining=int(dict_order["remaining"]),
            created_at=datetime.datetime.fromisoformat(dict_order["created_at"]),
        )


class TradeBot:
    """A trader capable of interacting with the api at /api."""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def place_order(self, symbol, price, side, quantity) -> Order | RequestError:
        """Place a new order. Returns either the created Order or a RequestError if the request
        fails.
        """
        logger.debug(f"Placing Order: {symbol}, {price}, {side}, {quantity}")

        try:
            price = decimal.Decimal(price)
            if price <= 0:
                logger.error("Invalid price: Price must be greater than 0")
                return RequestError(400, f"Invalid price: must be positive")
        except:
            logger.error("Invalid price: Price must be a valid integer")
            return RequestError(400, f"Invalid price: {price}")

        try:
            quantity = int(quantity)
            if quantity <= 0:
                logger.error("Invalid quantity: Quantity must be greater than 0")
                return RequestError(400, f"Invalid quantity: must be positive")
        except:
            logger.error("Invalid quantity: Quantity must be a valid integer")
            return RequestError(400, f"Invalid quantity: {quantity}")

        side = side.strip().upper()
        if side not in {"BUY", "SELL"}:
            logger.error("Invalid side: Side must be BUY or SELL")
            return RequestError(400, f"Invalid side: {side}")

        payload = {
            "symbol": symbol,
            "price": str(price),
            "side": side,
            "quantity": quantity
        }

        logger.info(f"Sending order: {payload}")
        print(json.dumps(payload, indent=4))

        response = requests.post(
            BASE_URL + "/orders",
            json=payload,
            auth=(self.username, self.password),
        )

        #print("\nStatus Code:", response.status_code)

        response_dict = response.json()

        if response.status_code not in (200, 201):
            err = RequestError(response.status_code, response.text)
            logger.error(f"Failed to send order! Response Status: {err}")
            return err

        order = Order.from_dict(response_dict)
        logger.info(f"JSON Order dictionary made into Order object: {order}")
        return order


    def get_orders(self) -> list[Order] | RequestError:
        """Get a list of the trader's currently open orders."""

        response = requests.get(
            url=BASE_URL + "/orders/open",
            auth=(self.username, self.password),
        )

        if response.status_code not in (200, 201):
            err = RequestError(response.status_code, response.text)
            return err

        orders: list[Order] = []

        list_dict_orders = response.json() # just raw list[dict[]]

        for dict_order in list_dict_orders:
            order = Order.from_dict(dict_order)
            orders.append(order)

        return orders

    def recent_trades(self) -> list[Trade] | RequestError:
        response = requests.get(
            url=BASE_URL + "/trades/recent",
            auth=(self.username, self.password),
        )

        trades: list[Trade] = []
        list_dict_trades = response.json()

        if isinstance(list_dict_trades, dict):
            return RequestError(response.status_code, list_dict_trades["detail"])

        for dict_trade in list_dict_trades:
            trade = Trade.from_dict(dict_trade)
            trades.append(trade)

        return trades


    def get_market(self) -> list[MarketReport] | RequestError:
        """Get a list of MarketReports outlining the state of the market."""

        response = requests.get(
            url=BASE_URL + "/market",
            auth=(self.username, self.password),
        )

        if response.status_code not in (200, 201):
            err = RequestError(response.status_code, response.text)
            print(err)
            return err

        market_reports: list[MarketReport] = [];
        list_dict_reports = response.json() # just raw list[dict[]]

        for dict_report in list_dict_reports:
            report = MarketReport.from_dict(dict_report)
            market_reports.append(report)

        return market_reports


def automatic_input(file_path, tradebots: dict[TeamName, TradeBot]):
    """Place orders from csv file at `file_path`, example:
    ```file_path.csv
    team,symbol,price,side,quantity
    "teamA","BEAR",10,"BUY",100
    ```
    """
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        for order_num,order_record in enumerate(reader):
            tradebot = tradebots.get(order_record["team"])
            if tradebot is None:
                print(f'Order #{order_num}: {order_record}')
                print(f'\tUnknown Trader: {order_record["team"]}')
                continue

            print("Posted:", tradebot.place_order(order_record["symbol"], order_record["price"],
                                                  order_record["side"], order_record["quantity"]))


def traders_from_csv(file_path) -> dict[TeamName, TradeBot]:
    """Load `TradeBot`s from csv file at `file_path`, example:
    ```file_path.csv
    username,password
    "teamA","team1234"
    "teamB","team1234"
    ```

    Returns a dictionary matching given usernames with their corresponding `TradeBot`.
    """
    tradebots = {}
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for trader in reader:
            tradebots[trader["username"]] = TradeBot(trader["username"], trader["password"])

    return tradebots


if __name__ == "__main__":
    tradebots = traders_from_csv("sample-traders.csv")
    for traderbot in tradebots.values():
        print()
        market = traderbot.get_market()
        if isinstance(market, RequestError):
            print(market)
            continue

        for report in market:
            print(report)

        trader = traderbot.username
        orders = traderbot.get_orders()
        recent_trades = traderbot.recent_trades()

        #traderbot.place_order("BEAR", 10, "SELL", 50)

        print(trader)

        if isinstance(orders, RequestError):
            print("Order Error")
            print(orders)
            continue

        for order in orders:
            print(order)
        for trade in recent_trades:
            print(trade)
        print("\n")

    exit()
    automatic_input("sample-auto-input.csv", tradebots)
    exit()
