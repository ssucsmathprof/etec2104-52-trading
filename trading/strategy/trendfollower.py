from tradebot import TradeBot
import time
from pylogger import get_logger
'''Trend follower: 
    If last trade price rises repeatedly-> bias to buy; 
    If it falls-> bias to sell.
'''

logger = get_logger()

price_history = {} # Will store symbols and there 3 most recent trade prices

trend_follower_bot = TradeBot(
    username="TrendFollower",
    password="team1234"
)
logger.info(f"Created Trend Follower Bot: {trend_follower_bot}")

def update_price_history(market_report):
    logger.debug("Update price history: "
                 "Adds a symbol to price_history dict if it wasn't there. "
                 "Updates each symbol's last three prices by appending the latest price, and removing"
                 "the oldest price."
                 "The price history of each symbol is kept to the last three prices")

    for report in market_report:
        symbol = report.symbol.code
        logger.info(f"Updating price history for {symbol}")
        price = report.last_price

        if symbol not in price_history:
            price_history[symbol] = []

        price_history[symbol].append(price)
        logger.info(f"Added {price} to {symbol} price history")

        if len(price_history[symbol]) > 3:
            logger.info(f"Removing oldest price ({price_history[symbol][0]}) from {symbol} price history")
            price_history[symbol].pop(0)

    logger.info(f"Updated price history: {price_history}")

def calculate_trend(symbol):
    logger.debug("Calculating price trend:"
                 "Looks at each symbols three recent prices"
                 "If there isn't three recent prices to look at, we don't have enough info so we wait."
                 "If there is an increase with each of the three prices->buy"
                 "If there is an decrease with each of the three prices->sell"
                 "If any of the latest prices equal or not ascending/descending, there is no trend to follower->wait")

    recent_prices = price_history.get(symbol, [])
    logger.info(f"Calculating price trend for {symbol}")
    logger.info(f"Recent prices: {recent_prices}")

    if len(recent_prices)< 3: # Not enough to see any trend
        logger.info("Not enough information for trend")
        return None

    elif recent_prices[-3] < recent_prices[-2] < recent_prices[-1]: # Price trends rise
        logger.info("Rising trend: Trend Follower biased to buy")
        return "BUY"
    elif recent_prices[-3] > recent_prices[-2] > recent_prices[-1]: # Price trends fall
        logger.info("Falling trend: Trend Follower biased to sell")
        return "SELL"
    else: # No trend
        logger.info("No trend calculated")
        return "WAIT"

def market_decision():
    logger.debug("Deciding if Trend Follower will buy/sell:"
                 "For each symbol, make a decision"
                 "The decision is decided by calculate_trend"
                 "If the decision is a BUY or SELL, TrendFollower will place and order")

    market_report = trend_follower_bot.get_market()
    update_price_history(market_report)

    for symbol in price_history:
        decision = calculate_trend(symbol)
        logger.info(f"{decision} at {symbol}")

        if decision in ("BUY", "SELL"):
            trend_follower_bot.place_order(
                symbol,
                price_history[symbol][2],
                decision,
                100
            )
            logger.info(f"Trend Follower places order: {symbol, price_history[symbol][2], decision, 100}")
#TODO(done): Tradebot needs to look at each symbols trend, and buy/sell/wait on each
#       symbol based off the calculated trend. (For each symbol, buy/sell/wait.)

#TODO: Run based off market ticks, and not seconds
while True:
    market_decision()
    time.sleep(5)