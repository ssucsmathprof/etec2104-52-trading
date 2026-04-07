from tradebot import TradeBot, Order
import random
import time
from pylogger import get_logger
'''RandomBot:
    Places orders randomly in the market.
    Good for testing
'''

logger = get_logger()

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
    random_index = random.randint(0, len(symbols_list)-1)
    return symbols_list[random_index]

def get_random_side():
    sides = ["BUY","SELL"]
    random_index = random.randint(0, 1)
    return sides[random_index]

def place_random_order():
    random_bot.place_order(
        symbol= get_random_symbol(),
        price=random.randint(1, 100),
        side= get_random_side(),
        quantity=random.randint(1, 100)
    )

while True:
    place_random_order()
    time.sleep(5)