import random
from str_universal import can_buy,place_order


class randomBot():
    def __init__(self, trader):
        mood = 0
        self.trader = trader


    def doStuff(self,mood):
        orders = []
        # random bs, go!
        if mood < 0.5:
            spread = random.randint(1, 3)
            size = random.randint(5, 20)

            if can_buy(self.trader):
                place_order(self.trader)

        # impulse
        if mood < 0.8:
            side = random.choice(["BUY", "SELL"])
            qty = random.randint(1, 25)
            if side == "BUY" and can_buy(self.trader):
                ...
            if side == "SELL":
                ...

        # Panik
        else:
            side = random.choice(["BUY", "SELL"])
            qty = random.randint(10, 40)

            if side == "BUY":
                if can_buy(self.trader):
                    ...
            else:
                ...
                #sell