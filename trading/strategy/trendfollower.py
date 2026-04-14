from tradebot import TradeBot
import time
from pylogger import get_logger
'''
Trend follower: 
    If last trade price rises repeatedly-> bias to buy; 
    If it falls-> bias to sell.
'''

logger = get_logger()

class TrendFollower:
    def __init__(self, username, password):
        self.bot = TradeBot(username=username, password=password)
        self.price_history = {}
        logger.info(f"Created TrendFollower Bot: {self.bot.username}")

    def update_price_history(self, market_report):
        logger.debug('''Update price history: "
                        Adds a symbol to price_history dict if it wasn't there. 
                        Updates each symbol's last three prices by appending the latest price, and removing
                        the oldest price.
                        The price history of each symbol is kept to the last three prices''')

        for report in market_report:
            symbol = report.symbol.code
            logger.info(f"Updating price history for {symbol}")
            price = report.last_price

            if symbol not in self.price_history:
                self.price_history[symbol] = []

            self.price_history[symbol].append(price)
            logger.info(f"Added {price} to {symbol} price history")

            if len(self.price_history[symbol]) > 3:
                logger.info(f"Removing oldest price ({self.price_history[symbol][0]}) from {symbol} price history")
                self.price_history[symbol].pop(0)

        logger.info(f"Updated price history: {self.price_history}")

    def calculate_trend(self, symbol):
        logger.debug('''Calculating price trend:
                        Looks at each symbols three recent prices
                        If there isn't three recent prices to look at, we don't have enough info so we wait.
                        If there is an increase with each of the three prices->buy
                        If there is an decrease with each of the three prices->sell
                        If any of the latest prices equal or not ascending/descending, there is no trend to follower->wait''')

        recent_prices = self.price_history.get(symbol, [])
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

    def market_decision(self):
        logger.debug('''Deciding if Trend Follower will buy/sell:
                        For each symbol, make a decision
                        The decision is decided by calculate_trend
                        If the decision is a BUY or SELL, TrendFollower will place and order''')

        market_report = self.bot.get_market()
        self.update_price_history(market_report)

        for symbol in self.price_history:
            decision = self.calculate_trend(symbol)
            logger.info(f"{decision} at {symbol}")

            if decision in ("BUY", "SELL"):
                try:
                    self.bot.place_order(
                        symbol,
                        self.price_history[symbol][2],
                        decision,
                        100
                    )
                    logger.info(f"Trend Follower places order: {symbol, self.price_history[symbol][2], decision, 100}")
                except:
                    logger.error(f"Trend Follower tried to place order: {symbol, self.price_history[symbol][2], decision, 100} and failed!")

    def run_trend_follower(self):
        logger.debug("Runs Trend Follower Bot by calling self.market_decision() and sleeping every 5 seconds")
        self.market_decision()
        logger.info(f"--------------------Running Trend Follower--------------------")
        time.sleep(5)

#TODO(done): Tradebot needs to look at each symbols trend, and buy/sell/wait on each
#       symbol based off the calculated trend. (For each symbol, buy/sell/wait.)
trend_follower = TrendFollower("TrendFollower", "team1234")

def main():
    while True:
        trend_follower.run_trend_follower()

if __name__ == "__main__":
    main()