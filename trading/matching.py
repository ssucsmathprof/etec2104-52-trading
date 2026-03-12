from decimal import Decimal
from django.db import transaction

from exchange.models import MarketPrice, Symbol
from trading.models import Order, Position, Trade, Trader

def get_position(trader, symbol):
    pos, _ = Position.objects.get_or_create(trader=trader, symbol=symbol, defaults={"shares": 0})
    return pos

@transaction.atomic
def match_symbol(symbol_code):
    symbol = Symbol.objects.get(code=symbol_code)

    # Best buy = highest price, earlier time
    # Best sell = lowest price, earlier time
    while True:
        buy = (
            Order.objects
            .select_for_update()
            .filter(symbol=symbol, side="BUY", remaining__gt=0)
            .order_by("-price", "created_at")
            .first()
        )
        sell = (
            Order.objects
            .select_for_update()
            .filter(symbol=symbol, side="SELL", remaining__gt=0)
            .order_by("price", "created_at")
            .first()
        )

        if not buy or not sell:
            break

        # Crossing?
        if buy.price < sell.price:
            break

        qty = min(buy.remaining, sell.remaining)

        # trade at sell price (simple rule)
        trade_price = Decimal(sell.price)
        cost = trade_price * qty

        buyer = buy.trader
        seller = sell.trader

        # enforce: no short selling + must have cash
        buyer = Trader.objects.select_for_update().get(id=buyer.id)
        seller = Trader.objects.select_for_update().get(id=seller.id)

        if buyer.cash < cost:
            # cancel buy if cannot pay
            buy.remaining = 0
            buy.save(update_fields=["remaining"])
            continue

        seller_pos = get_position(seller, symbol)
        # if seller_pos.shares < qty:
        #     # cancel sell if cannot deliver shares
        #     sell.remaining = 0
        #     sell.save(update_fields=["remaining"])
        #     continue

        # apply cash + shares
        buyer.cash -= cost
        seller.cash += cost
        buyer.save(update_fields=["cash"])
        seller.save(update_fields=["cash"])

        buyer_pos = get_position(buyer, symbol)
        buyer_pos.shares += qty
        seller_pos.shares -= qty
        buyer_pos.save(update_fields=["shares"])
        seller_pos.save(update_fields=["shares"])

        # decrement remaining
        buy.remaining -= qty
        sell.remaining -= qty
        buy.save(update_fields=["remaining"])
        sell.save(update_fields=["remaining"])

        Trade.objects.create(
            symbol=symbol,
            price=trade_price,
            quantity=qty,
            buyer=buyer,
            seller=seller,
        )

        # update last price
        MarketPrice.objects.update_or_create(symbol=symbol, defaults={"last_price": trade_price})
