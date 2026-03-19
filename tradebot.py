
import requests
import json
import sys
import csv

BASE_URL = "http://127.0.0.1:8000/api"

type TeamName = str

class TradeBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def place_order(self, symbol, price, side, quantity):
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

        print("\nStatus Code:", response.status_code)

        try:
            print(json.dumps(response.json(), indent=4))
            return response.json()
        except Exception:
            print(response.text)
            return None


    def get_orders(self):
        response = requests.get(
            url=BASE_URL + "/orders/open",
            auth=(self.username, self.password),
        )
        return response.json() # just raw list[dict[]]

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

            tradebot.place_order(order_record["symbol"], order_record["price"],
                                  order_record["side"], order_record["quantity"])


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
        print(traderbot.get_orders())

    exit()
    automatic_input("sample-auto-input.csv", tradebots)
    exit()
