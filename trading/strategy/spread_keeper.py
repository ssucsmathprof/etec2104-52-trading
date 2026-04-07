"""Spread Keeper Strategy
Tries to always maintain one bid and one ask around the inside market.
"""

from typing import List, Dict
import decimal
from logging import Logger

from tradebot import TradeBot, RequestError, MarketReport, Order

from pylogger import get_logger

logger: Logger = get_logger()

class SpreadKeeper:
    tradebot: TradeBot
    placement_threshold: decimal.Decimal
    """Strategy tries to keep orders within this distance from market price"""

    def __init__(self, tradebot: TradeBot, placement_threshold: decimal.Decimal | int | float =5):
        self.tradebot = tradebot
        self.placement_threshold = decimal.Decimal(placement_threshold)
        logger.debug(f"Created new SpreadKeeper strategy: {self}")

    def transform_market_reports(market_reports: List[MarketReport]) -> Dict[str, MarketReport]:
        """Turn a list of reports into a dictionary of reports indexed by symbol code."""

        reports = {}

        for report in market_reports:
            reports[report.symbol.code] = report

        return reports

    def handle_market(self, report: MarketReport, open_orders: List[Order]):
        logger.info(
            f"SpreadKeeper: Checking for orders near market price in "
            f"{report.symbol.code}@{report.last_price}"
        )

        orders_within = {"BUY": 0, "SELL": 0}

        for order in open_orders:
            if order.symbol != report.symbol.code:
                continue

            distance = report.last_price - order.price
            if distance > self.placement_threshold:
                continue

            orders_within[order.side] += 1

        for side, num_orders in orders_within.items():
            logger.info(
                f"SpreadKeeper: {report.symbol.code}@{report.last_price}: "
                f"Found {num_orders} {side}{'s' if num_orders != 1 else ''} "
                "within threshold of market price"
            )

            if side == "BUY":
                price = report.last_price - self.placement_threshold
            if side == "SELL":
                price = report.last_price + self.placement_threshold

            if num_orders == 0:
                quantity = 100 # arbitrary
                response = self.tradebot.place_order(report.symbol.code, price, side, quantity)
                if isinstance(response, RequestError):
                    logger.error(
                        f"SpreadKeeper: {report.symbol.code}@{report.last_price}: "
                        f"Failed to submit {side}@{price} for {quantity}"
                    )

    def tick(self):
        logger.info(f"SpreadKeeper: Starting tick")

        market_reports = self.tradebot.get_market()
        if isinstance(market_reports, RequestError):
            logger.error(f"SpreadKeeper: Aborting Tick: Failed to get market reports")
            return

        open_orders = self.tradebot.get_orders()
        if isinstance(open_orders, RequestError):
            logger.error(f"SpreadKeeper: Aborting Tick: Failed to get open orders")
            return

        for report in market_reports:
            self.handle_market(report, open_orders)

def main():
    print("TESTING SpreadKeeper strategy")

    spread_threshold = 2
    market = "TEST"
    # have teamA keep the spread, and use teamB to manip. market
    team_a = SpreadKeeper(TradeBot("teamA", "team1234"), spread_threshold)
    team_b = TradeBot("teamB", "team1234")

    # ensure there's a last price in BEAR at 10
    team_a.tradebot.place_order(market, 10, "BUY", 10)
    team_b.place_order(market, 10, "SELL", 10)

    team_a.tick()

    def get_applicable_orders(order: Order) -> bool:
        return abs(10 - order.price) <= spread_threshold and order.symbol == market

    def check():
        open_orders = team_a.tradebot.get_orders()
        if isinstance(open_orders, RequestError):
            print("Couldn't get open orders! >:[")
            return False

        orders_in_threshold = list(filter(get_applicable_orders, open_orders))
        if len(orders_in_threshold) != 2:
            print(f"EXPECTED 2 orders at the threshold. FOUND {len(orders_in_threshold)}")
            for order in orders_in_threshold:
                print(order)
            return False

        return True

    if not check(): return

    team_b.place_order(market, 12, "BUY", 10)
    team_a.tick()
    if not check(): return

    team_b.place_order(market, 8, "SELL", 10)
    team_a.tick()
    if not check(): return

    print("TESTING SpreadKeeper strategy: Passes!")

if __name__ == "__main__":
    main()

