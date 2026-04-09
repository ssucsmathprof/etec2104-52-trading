from tradebot import TradeBot
import time
from pylogger import get_logger
'''
Market Maker: 
    Buys at price - 1
    Sells at price + 1
'''

logger = get_logger()

market_maker_bot = TradeBot(
    username="MarketMaker",
    password="team1234"
)
logger.info(f"Created Market Maker Bot: {market_maker_bot}")

last_symbol_prices = {}

def get_latest_prices():
    logger.debug('''Gets latest price for each symbol."
                    Adds a symbol to the dict if not
                    already in dict. 
                    Removes price to only associate most recent price
                    per symbol.''')
    market_report = market_maker_bot.get_market()

    for report in market_report:
        symbol = report.symbol.code
        price = report.last_price

        if symbol not in last_symbol_prices:
            last_symbol_prices[symbol] = []

        if len(last_symbol_prices[symbol]) >= 1:
            last_symbol_prices[symbol].pop(0)
        last_symbol_prices[symbol].append(price)
    logger.info(f"Latest prices for all symbols: {last_symbol_prices}")

def buy_order(symbol):
    logger.debug('''Places an buy order for a symbol that has a price
                        of one less than that symbols last price.''')
    last_price = last_symbol_prices[symbol][-1]

    market_maker_bot.place_order(
        symbol = symbol,
        price = last_price - 1,
        side = "BUY",
        quantity = 100,
    )
    logger.info(f"Market Maker Placed Order: {symbol, last_price - 1, "BUY", 100}")

def sell_order(symbol):
    logger.debug('''Places an sell order for a symbol that has a price
                    of one more than that symbols last price.''')
    last_price = last_symbol_prices[symbol][-1]

    market_maker_bot.place_order(
        symbol = symbol,
        price = last_price + 1,
        side = "SELL",
        quantity = 100,
    )
    logger.info(f"Market Maker Placed Order: {symbol, last_price+1, "SELL", 100}")

def market_maker():
    logger.debug('''Makes a buy order for every symbol at one less the latest price.
                    Makes a sell order for every symbol at one more the latest price price.''')
    get_latest_prices()

    for symbol in last_symbol_prices:
        buy_order(symbol)
        sell_order(symbol)
    time.sleep(5)

while True:
    market_maker()