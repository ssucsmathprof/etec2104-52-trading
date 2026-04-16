import randomtradebot
from str_universal import *
from Strategy_Objects import *


class randomBot():
    def __init__(self, Trader):
        self.trader = Trader
        self.mood = random.random() #this is basically just what makes choices


    def doStuff(self,symbol,price,orderbook):
        self.mood = random.random()
        # buy,buy,buy!
        if self.mood < 0.4:
            side = "BUY"
            qty = random.randint(1, 100)
            print("BUY BUY BUY!!!!!\n")
            if self.trader.can_afford(price, qty) and side == "BUY":
                place_order(self.trader,
                            symbol,price,side,qty)

        # impulse sell
        if self.mood > 0.4 and self.mood < 0.89:
            side = "SELL"
            qty = random.randint(1, 25)
            print("I am selling because lol. lmao even.\n")
            if side == "SELL":
                place_order(self.trader,
                            symbol,price,"SELL",qty)

        # Smart... maybe
        else:
            qty = random.randint(1, 40)
            orderMoney = orderbook.get_youngest_order(symbol)
            print("I was never book smart im money smart, makes me more intel- more intelligent.\n"
                  "Call me mister rock festival i got hella bands,\n shawty cute her circle too tell her get a friend\n")
            if orderMoney.price*orderMoney.quantity < get_recent_orders(self.trader):
                side = "BUY"
                if self.trader.can_afford(price, qty) and side == "BUY":
                    place_order(self.trader,
                                symbol,price,side,qty)
            elif orderMoney*orderMoney.quantity >= get_recent_orders(self.trader):
                side = "SELL"
                if side == "SELL":
                    place_order(self.trader,
                                symbol,price,side,qty)
    def testMe(self,orderbook):
        randomSymbol = random.choice("BEAR","MUTTON", "SQUAB", "VEAL", "VENISON")
        randomBot.doStuff(randomSymbol,orderbook,orderbook)
        print("tested stuff :)")