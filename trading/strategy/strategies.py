
import random
import request
import str_universal



def random_strategy(team, symbols, exchange_state, traders):
    orders = []
    s = random.choice(symbols)
    side = random.choice(["buy", "sell"])

    ret = request.get(url, auth=(trader.username, trader.passowrd))

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

def decide_order(trader_state, market_snapshot):
    orders = []
    team = trader_state["team"]

    symbol = random.choice(str_universal.SYMBOLS)

    ltp = None
    if "last_trade" in market_snapshot:
        ltp = market_snapshot["last_trade"].get(symbol)
    if ltp is None:
        ltp = random.randint(98, 102)

    cash = trader_state["cash"]
    position = trader_state["shares"].get(symbol, 0)
    # i wanted the trades to be silly and random
    mood = random.random()

    def can_buy(price, qty):
        return cash >= price * qty

    def can_sell(qty):
        return position >= qty

    # Zzzzzzzzzzzz
    if mood < 0.2:
        return []

    # random bs, go!
    elif mood < 0.5:
        spread = random.randint(1, 3)
        size = random.randint(5, 20)

        buy_price = ltp - spread
        sell_price = ltp + spread

        if can_buy(buy_price, size):
            orders.append({
                "team": team,
                "symbol": symbol,
                "side": "BUY",
                "price": buy_price,
                "qty": size,
            })

        if can_sell(size):
            orders.append({
                "team": team,
                "symbol": symbol,
                "side": "SELL",
                "price": sell_price,
                "qty": size,
            })

    # impulse
    elif mood < 0.8:
        side = random.choice(["BUY", "SELL"])
        price = ltp + random.randint(-4, 4)
        qty = random.randint(1, 25)

        if side == "BUY" and can_buy(price, qty):
            orders.append({
                "team": team,
                "symbol": symbol,
                "side": "BUY",
                "price": price,
                "qty": qty,
            })

        if side == "SELL" and can_sell(qty):
            orders.append({
                "team": team,
                "symbol": symbol,
                "side": "SELL",
                "price": price,
                "qty": qty,
            })

    # Panik
    else:
        side = random.choice(["BUY", "SELL"])
        qty = random.randint(10, 40)

        if side == "BUY":
            price = ltp + random.randint(2, 6)
            if can_buy(price, qty):
                orders.append({
                    "team": team,
                    "symbol": symbol,
                    "side": "BUY",
                    "price": price,
                    "qty": qty,
                })
        else:
            price = ltp - random.randint(2, 6)
            if can_sell(qty):
                orders.append({
                    "team": team,
                    "symbol": symbol,
                    "side": "SELL",
                    "price": price,
                    "qty": qty,
                })

    return orders
