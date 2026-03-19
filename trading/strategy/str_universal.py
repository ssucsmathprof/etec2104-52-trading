SYMBOLS = ['BEAR', 'FROG', 'LZRD']
SIDES = ("BUY", "SELL")



def make_order(team, side, symbol, price, qty):
    return {
        "team": team,
        "side": side,
        "symbol": symbol,
        "price": float(price),
        "qty": int(qty),
    }

def make_trade(buyer, seller, symbol, price, qty):
    return {
        "buyer": buyer,
        "seller": seller,
        "symbol": symbol,
        "price": float(price),
        "qty": int(qty),
    }

def get_url(base_url, task):
    return