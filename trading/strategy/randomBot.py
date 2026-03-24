import random
from str_universal import *


class randomBot():
    def __init__(self, trader):
        mood = 0 #this is basically just what makes choices
        self.trader = trader


    def doStuff(self,mood):
        mood = random.random()
        # buy,buy,buy!
        if mood < 0.5:
            side = "BUY"
            qty = random.randint(10, 40)

            if can_buy(self.trader):
                place_order(self.trader.user.username,
                            symbol,price,side,qty)

        # impulse
        if mood < 0.8:
            side = random.choice(["BUY", "SELL"])
            qty = random.randint(1, 25)
            if side == "BUY" and can_buy(self.trader):
                place_order(self.trader.user.username,
                            symbol, price,"BUY", qty)
            if side == "SELL":
                place_order(self.trader.user.username,
                            symbol, price,"SELL", qty)

        # Smart
        else:
            side = random.choice(["BUY", "SELL"])
            qty = random.randint(10, 40)

            if side == "BUY":
                if can_buy(self.trader):
                    place_order(self.trader.user.username,
                                symbol, price, side, qty)
            if side == "SELL":
                place_order(self.trader.user.username,
                            symbol,price,side,qty)