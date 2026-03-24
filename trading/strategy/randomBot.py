import random

class randomBot(object):
    def __init__(self):
        mood = 0

    def doStuff(self,mood):
        # random bs, go!
        if mood < 0.5:
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