"""Spread Keeper Strategy
Tries to always maintain one bid and one ask around the inside market.
"""

from typing import List, Dict, Literal
import decimal
from logging import Logger

from tradebot import TradeBot, RequestError, MarketReport, Order
from pylogger import get_logger

logger: Logger = get_logger()

class SpreadKeeper:
    """Tries to always maintain one bid and one ask around the inside market."""

    tradebot: TradeBot
    placement_threshold: decimal.Decimal
    """Strategy tries to keep orders within this distance from market price"""

    def __init__(self, tradebot: TradeBot, placement_threshold: decimal.Decimal | int | float =5):
        self.tradebot = tradebot
        self.placement_threshold = decimal.Decimal(placement_threshold)
        logger.debug(f"Created new SpreadKeeper strategy: {self}")

    def _get_target_price(self, report: MarketReport, side):
        if side == "BUY":
            return report.last_price - self.placement_threshold
        if side == "SELL":
            return report.last_price + self.placement_threshold


    def _cancel_extraneous_orders(self, report: MarketReport, orders: List[Order]):
        if len(orders) == 0:
            return

        price = self._get_target_price(report, orders[0].side)

        # sort orders such that the closest order to the desired price is first
        orders = sorted(orders, key=lambda order: abs(order.price - price))

        # cancel all orders except the best
        if len(orders) > 1:
            logger.info(f"SpreadKeeper: {report.symbol.code}@{report.last_price}: "
                        "Cancelling extraneous orders inside threshold")
            for order in orders[1:]:
                #response = self.tradebot.cancel(order)
                response = RequestError(0, "The exchange doesn't implement this yet!")
                if isinstance(response, RequestError):
                    logger.error(
                        f"SpreadKeeper: {report.symbol.code}@{report.last_price}: "
                        f"Failed to cancel order: {order}"
                    )

    def _place_order(self, report: MarketReport, side):
        price = self._get_target_price(report, side)

        quantity = 100 # arbitrary
        response = self.tradebot.place_order(report.symbol.code, price, side, quantity)
        if isinstance(response, RequestError):
            logger.error(
                f"SpreadKeeper: {report.symbol.code}@{report.last_price}: "
                f"Failed to submit {side}@{price} for {quantity}"
            )

    def _keep_orders_at_threshold(self, report: MarketReport, side, orders: list[Order]):
        num_orders = len(orders)
        logger.info(
            f"SpreadKeeper: {report.symbol.code}@{report.last_price}: "
            f"Found {num_orders} {side}{'s' if num_orders != 1 else ''} "
            f"within threshold of market price (+/- {self.placement_threshold})"
        )

        self._cancel_extraneous_orders(report, orders)

        if num_orders == 0:
            logger.info(f"SpreadKeeper: {report.symbol.code}@{report.last_price}: "
                        f"No orders within threshold (+/- {self.placement_threshold}), placing new order")
            self._place_order(report, side)


    def _handle_market(self, report: MarketReport, open_orders: List[Order]):
        logger.info(
            f"SpreadKeeper: Checking for orders near market price in "
            f"{report.symbol.code}@{report.last_price}"
        )

        orders_within = {"BUY": [], "SELL": []}

        for order in open_orders:
            if order.symbol != report.symbol.code:
                continue

            distance = report.last_price - order.price
            if distance > self.placement_threshold:
                continue

            orders_within[order.side].append(order)

        for side, orders in orders_within.items():
            self._keep_orders_at_threshold(report, side, orders)

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
            self._handle_market(report, open_orders)

def main():
    """Assumes market TEST is tradeable by teamA and teamB and that both traders have
    password='team1234'. teamA runs the spreadkeeper strategy and teamB is used to manipulate the
    market.

    SpreadKeeper tries to cancel orders, but until that logic is actually implemented, this test can
    fail on pre-populated markets.

    Testing can also be done interactively by just repeatedly ticking a bot with the strategy and
    manually sending in orders to manipulate the market:

    ```test-script.py
    from time import sleep
    import tradebot
    from trading.strategy import spread_keeper

    strat = spread_keeper.SpreadKeeper(tradebot.TradeBot("teamA", "team1234"))

    while True:
        strat.tick()
        sleep(1)
    ```
    """

    print("TESTING SpreadKeeper strategy")

    spread_threshold = 2
    market_code = "TEST"

    team_a = SpreadKeeper(TradeBot("teamA", "team1234"), spread_threshold)
    team_b = TradeBot("teamB", "team1234")

    def get_market_price():
        market_reports = team_b.get_market()
        if isinstance(market_reports, RequestError):
            print("Couldn't get market reports! >:[")
            return False
        market_report = [report for report in market_reports if report.symbol.code == market_code]
        if (len(market_report) == 0):
            return None;

        return market_report[0].last_price

    # make sure market has price
    if (get_market_price() is None):
        print("Creating initial market")
        team_a.tradebot.place_order(market_code, 10, "BUY", 10)
        team_b.place_order(market_code, 10, "SELL", 10)

    team_a.tick()

    def get_applicable_orders(order: Order) -> bool:
        return abs(get_market_price() - order.price) <= spread_threshold and order.symbol == market_code

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

    team_b.place_order(market_code, get_market_price() + spread_threshold, "BUY", 10)
    team_a.tick()
    if not check(): return

    team_b.place_order(market_code, get_market_price() - spread_threshold, "SELL", 10)
    team_a.tick()
    if not check(): return

    print("TESTING SpreadKeeper strategy: Passes!")

if __name__ == "__main__":
    main()

