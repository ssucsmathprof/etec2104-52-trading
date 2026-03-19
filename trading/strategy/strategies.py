
import random

def random_strategy(team, symbols, exchange_state, traders):
    orders = []
    s = random.choice(symbols)
    side = random.choice(["buy", "sell"])

    last = exchange_state["last_trade"][s]
    if last is None:
        price = random.randint(5, 15)
    else:
        price = max(1, last + random.randint(-2, 2))

    qty = random.randint(1, 50)

    if side == "buy":
        if traders[team]["cash"] < price * qty:
            return orders
    else:
        if traders[team]["positions"][s] < qty:
            return orders

    orders.append({
        "team": team,
        "symbol": s,
        "side": side,
        "price": float(price),
        "quantity": qty
    })
    return orders


def hilo_strategy(team, symbols, exchange_state, traders):
    orders = []
    s = random.choice(symbols)
    #side = random.choice(["buy", "sell"])

    last = exchange_state["last_trade"][s]
    if last is None:
        return orders
    else:
        price = last

    qty = 1
    if price <= 8:
        side = 'buy'
    elif price >= 12:
        side = 'sell'
    else:
        return orders
    if side == "buy":
        if traders[team]["cash"] < price * qty:
            return orders
    else:
        if traders[team]["positions"][s] < qty:
            return orders

    orders.append({
        "team": team,
        "symbol": s,
        "side": side,
        "price": float(price),
        "quantity": qty
    })
    return orders