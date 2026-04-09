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

random_bot = TradeBot(
    username="RandomBot",
    password="team1234"
)

# Generate list of symbols
symbols_list = []
market_report = random_bot.get_market()
for report in market_report:
    symbol = report.symbol.code
    symbols_list.append(symbol)

def get_random_symbol():
    logger.debug("Randomly picks a symbol from the list of symbols")
    random_index = random.randint(0, len(symbols_list)-1)
    return symbols_list[random_index]

def get_random_side():
    logger.debug("Randomly picks a side from either BUY or SELL")
    sides = ["BUY","SELL"]
    random_index = random.randint(0, 1)
    return sides[random_index]

def place_random_order():
    logger.debug("Places a random order with a random symbol, price, side, and quantity")
    random_price = random.randint(ORDER_MIN_PRICE, ORDER_MAX_PRICE)
    random_quantity = random.randint(ORDER_MIN_QUANTITY, ORDER_MAX_QUANTITY)
    random_bot.place_order(
        symbol= get_random_symbol(),
        price=random_price,
        side= get_random_side(),
        quantity=random_quantity
    )
    logger.info(f"Random TradeBot placed random order: {get_random_symbol(), random_price, get_random_side(), random_quantity}")

def run_random_tradebot(num_ticks=TRADE_COUNT):
    logger.debug("Runs random tradebot every")
    for step in range(num_ticks):
        place_random_order()
        time.sleep(TRADE_FREQUENCY)

while True:
    run_random_tradebot(num_ticks=TRADE_COUNT)