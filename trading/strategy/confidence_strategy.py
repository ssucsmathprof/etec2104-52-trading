from compression.zstd import Strategy
from trading import models
from strategies import str_universal as strat

class ConfidenceSellStrategy():


    def __init__(self, confidence, order):
        self.confidence = confidence
        self.my_order = order
        self.margin_of_error = 0

    def raise_confidence(self):
        pass

    def lower_confidence(self):
        pass

    def check_recent_trend(self):
        current_market = strat.get_market_picture()


        for order in current_market.orders:
            if order.symbol == self.my_order.symbol:
                if order.price >= self.my_order.price:
                    self.raise_confidence()
                else:
                    self.lower_confidence()

    def should_i_sell(self):
