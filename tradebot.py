import decimal
from typing import NamedTuple
import datetime
import requests
import json
import sys
import csv

BASE_URL = "http://127.0.0.1:8000/api"

type TeamName = str


class RequestError(NamedTuple):
    status_code: int
    detail: str

class Symbol(NamedTuple):
    id: int
    code: str

    def from_dict(dict_symbol: dict):
        return Symbol(
            id=dict_symbol["id"],
            code=dict_symbol["code"],
        )

class MarketReport(NamedTuple):
    id: int
    symbol: Symbol
    last_price: decimal.Decimal
    updated_at: datetime.datetime

    def from_dict(dict_market: dict):
        return MarketReport(
            id=dict_market["id"],
            symbol=Symbol.from_dict(dict_market["symbol"]),
            last_price=decimal.Decimal(dict_market["last_price"]),
            updated_at=datetime.datetime.fromisoformat(dict_market["updated_at"]),
        )


class Order(NamedTuple):
    id: int
    trader: TeamName
    symbol: str
    side: str
    price: decimal.Decimal
    quantity: int
    remaining: int
    created_at: datetime.datetime

    def from_dict(dict_order: dict):
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
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def place_order(self, symbol, price, side, quantity) -> Order | RequestError:
        payload = {
            "symbol": symbol,
            "price": price,
            "side": side,
            "quantity": quantity
        }

        print("Sending order:")
        print(json.dumps(payload, indent=4))

        response = requests.post(
            BASE_URL + "/orders",
            json=payload,
            auth=(self.username, self.password),
        )

        #print("\nStatus Code:", response.status_code)

        response_dict = response.json()

        if response_dict.get("detail") is not None:
            err = RequestError(response.status_code, response_dict["detail"])
            print(err)
            return err

        order = Order.from_dict(response_dict)
        #print(order)
        return order


    def get_orders(self) -> list[Order] | RequestError:
        response = requests.get(
            url=BASE_URL + "/orders/open",
            auth=(self.username, self.password),
        )
        orders: list[Order] = [];
        list_dict_orders = response.json() # just raw list[dict[]]

        # If request went wrong, response will be dict, not list
        if isinstance(list_dict_orders, dict):
            return RequestError(response.status_code, list_dict_orders["detail"])

        for dict_order in list_dict_orders:
            order = Order.from_dict(dict_order)
            orders.append(order)

        return orders


    def get_market(self) -> list[MarketReport] | RequestError:
        response = requests.get(
            url=BASE_URL + "/market",
            auth=(self.username, self.password),
        )
        market_reports: list[MarketReport] = [];
        list_dict_reports = response.json() # just raw list[dict[]]

        # If request went wrong, response will be dict, not list
        # (Though I'm not sure when this would error)
        if isinstance(list_dict_reports, dict):
            return RequestError(response.status_code, list_dict_reports["detail"])

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

    exit()
    automatic_input("sample-auto-input.csv", tradebots)
    exit()
