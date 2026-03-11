
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/orders"
USERNAME = "admin"
PASSWORD = "admin"

def place_order(symbol, price, side, quantity):
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
        auth=(USERNAME, PASSWORD),
    )

    print("\nStatus Code:", response.status_code)

    try:
        print(json.dumps(response.json(), indent=4))
    except Exception:
        print(response.text)

if __name__ == "__main__":

    symbol = "BEAR"
    price = 101
    side = "SELL"
    quantity = 10

    if len(sys.argv) == 5:
        symbol = sys.argv[1]
        price = float(sys.argv[2])
        side = sys.argv[3].upper()
        quantity = int(sys.argv[4])

    place_order(symbol, price, side, quantity)
