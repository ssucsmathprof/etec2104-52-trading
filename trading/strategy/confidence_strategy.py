from compression.zstd import Strategy
from trading import models
from strategies import str_universal as strat

CONFIDENCE_WEIGHT = 1.4

class ConfidenceSellStrategy():
    def __init__(self, trader, max_confidence, order, sell_goal):

        ## PUBLIC ATTRIBUTES
        self.current_nervousness = 0
        self.max_confidence = max_confidence
        self.my_order = order
        self.sell_goal = sell_goal

        ## PRIVATE ATTRIBUTES
        self.margin_of_error = 0
        self.newest_order = None
        self._my_trader = trader
        self._going_rate = 0

    def adjust_confidence(self, value):
        self.current_nervousness += value * CONFIDENCE_WEIGHT

        # Clamp to non-negative
        self.current_nervousness = max(0, self.current_nervousness)

    def is_order_newer(self, order):
        if self.newest_order == None:
            return True
        return self.newest_order.created_at < order.created_at

    def check_recent_trend(self):
        current_market = strat.get_orderbook_orders()
        for order in current_market:
            if order.symbol == self.my_order.symbol and self.is_order_newer(order):

                difference = self.my_order.price - order.price
                self.adjust_confidence(difference)

        self.newest_order = strat.TheOrderBook.get_youngest_order

    def should_i_sell(self):

        if self.current_nervousness >= self.max_confidence:
            return True
        current_market = strat.get_orderbook_orders()
        for order in current_market:
            if order.symbol == self.my_order.symbol:
                if order.price >= self.sell_goal:
                    return True
        return False

    def update_strategy(self):
        self.check_recent_trend()
        if self.should_i_sell():
            print("Selling My Stock")
            best_rate = strat.get_best_rate(self.my_order.symbol)
            strat.place_order(self._my_trader, self.my_order.symbol, best_rate, "SELL", self.my_order.quantity)
        else:
            print("Waiting for My Stock to be worth more")

