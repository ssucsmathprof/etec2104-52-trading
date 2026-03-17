
import requests
import json
import sys
import csv

BASE_URL = "http://127.0.0.1:8000/api/orders"

class TraderBot:
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
            BASE_URL,
            json=payload,
            auth=(self.username, self.password),
        )

        print("\nStatus Code:", response.status_code)

        try:
            print(json.dumps(response.json(), indent=4))
        except Exception:
            print(response.text)

    def get_orders(self):
        response = requests.get(
            url=BASE_URL + "/open",
            auth=(self.username, self.password),
        )
        return response.json() # just raw list[dict[]]

type TeamName = str
def automatic_input(file_path, traderbots: dict[TeamName, TraderBot]):
    """Place orders from csv file at `file_path`, example:
    ```file_path.csv
    team,symbol,price,side,quantity
    "teamA","BEAR",10,"BUY",100
    ```
    """
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        for order_num,order_record in enumerate(reader):
            traderbot = traderbots.get(order_record["team"])
            if traderbot is None:
                print(f'Order #{order_num}: {order_record}')
                print(f'\tUnknown Trader: {order_record["team"]}')
                continue

            traderbot.place_order(order_record["symbol"], order_record["price"],
                                  order_record["side"], order_record["quantity"])


if __name__ == "__main__":

    traderbots = {
        "teamA": TraderBot("teamA","team1234"),
        "teamB": TraderBot("teamB","team1234"),
    }

    for traderbot in traderbots.values():
        traderbot.get_orders()

    exit()
    automatic_input("sample-auto-input.csv", traderbots)
    exit()
