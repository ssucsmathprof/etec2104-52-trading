from tradebot import TradeBot
import random
import time
from pylogger import get_logger

'''
RandomBot:
    Places orders randomly in the market.
    Good for testing
'''

logger = get_logger()

# Range of random prices for the random order
ORDER_MIN_PRICE = 50
ORDER_MAX_PRICE = 100

# Range of random quantity for the random order
ORDER_MIN_QUANTITY = 50
ORDER_MAX_QUANTITY = 100

# Amount of trades Random TradeBot will run; will trade TRADE_COUNT amount of trades before stopping
TRADE_COUNT = 1000

# How often TradeBot runs; trades every TRADE_FREQUENCY seconds
TRADE_FREQUENCY = 5

class RandomBot:
    def __init__(self, username, password):
        self.bot = TradeBot(username=username, password=password)
        self.symbols_list = []
        self.market_report = self.bot.get_market()
        logger.info(f"Created Random Bot: {self.bot.username}")

    def generate_symbol_list(self):
        logger.debug("Generates the list of all symbols in the market")
        for report in self.market_report:
            symbol = report.symbol.code
            self.symbols_list.append(symbol)

    def get_random_symbol(self):
        logger.debug("Randomly picks a symbol from the list of symbols")
        random_index = random.randint(0, len(self.symbols_list) - 1)
        return self.symbols_list[random_index]

    def get_random_side(self):
        logger.debug("Randomly picks a side from either BUY or SELL")
        sides = ["BUY", "SELL"]
        random_index = random.randint(0, 1)
        return sides[random_index]

    def place_random_order(self):
        logger.debug("Places a random order with a random symbol, price, side, and quantity")
        random_price = random.randint(ORDER_MIN_PRICE, ORDER_MAX_PRICE)
        random_quantity = random.randint(ORDER_MIN_QUANTITY, ORDER_MAX_QUANTITY)
        self.bot.place_order(
            symbol=self.get_random_symbol(),
            price=random_price,
            side=self.get_random_side(),
            quantity=random_quantity
        )
        logger.info(
            f"Random TradeBot placed random order: {self.get_random_symbol(), random_price, self.get_random_side(), random_quantity}")

    def run_random_tradebot(self, num_ticks=TRADE_COUNT):
        logger.debug("Runs random tradebot every")
        for step in range(num_ticks):
            self.place_random_order()
            time.sleep(TRADE_FREQUENCY)

def main():
    randomBot = RandomBot("RandomBot", "team1234")
    randomBot.generate_symbol_list()

    while True:
        randomBot.run_random_tradebot(num_ticks=TRADE_COUNT)

if __name__ == "__main__":
    main()