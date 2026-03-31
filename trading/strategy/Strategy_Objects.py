
## Turn to False if a Trader isn't allowed to Sell with no Stocks
SELL_NO_STOCKS = True

class OrderBook:
    def __init__(self, order_list):
        '''
        Creates OrderBook instance from a list of orders.
        order_list: list of Order objects
        '''
        self.order_list = order_list
        self.youngest_order = None
        self.oldest_order = None

        self.set_oldest_and_youngest_order()

    def set_oldest_and_youngest_order(self):
        '''
        Sets the oldest order and youngest order in the OrderBook.
        '''
        if len(self.order_list) == 0:
            self.youngest_order = None
            self.oldest_order = None
            return
        for order in self.order_list:
            self.check_order_age(order)


    def check_order_age(self, order):
        '''
        Changes the oldest order and youngest order in the OrderBook if the order is older or younger.
        order: Order object
        '''
        if self.oldest_order is None or order.created_at < self.oldest_order.created_at:
            self.oldest_order = order

        if self.youngest_order is None or order.created_at > self.youngest_order.created_at:
            self.youngest_order = order

    def append(self, new_order):
        '''
        Adds a new order to the OrderBook if the order isn't in the OrderBook yet.
        new_order: new_order object.
        '''

        if not self.in_order_book(new_order):
            self.check_order_age(new_order)
            self.order_list.append(new_order)

    def get_oldest_order(self, symbol=None):
        '''
        Returns the oldest order in the OrderBook of some symbol, or the oldest if symbol is None.
        '''

        if symbol is None:
            return self.oldest_order

        oldest_order = None
        for order in self.order_list:
            if order.symbol == symbol:
                if oldest_order is None:
                    if order.created_art < oldest_order:
                        oldest_order = order
        return oldest_order




    def get_youngest_order(self, symbol=None):
        '''
        Returns the youngest order in the OrderBook of some symbol, or the youngest if symbol is None.
        '''

        if symbol is None:
            return self.youngest_order

        youngest_order = None
        for order in self.order_list:
            if order.symbol == symbol:
                if youngest_order is None:
                    if order.created_art > youngest_order:
                        youngest_order = order
        return youngest_order


    def in_order_book(self, order):
        '''
        Returns True if the order is in the OrderBook.
        '''
        return order in self.order_list

    def get_all_orders(self):
        '''
        Returns a list of all orders in the OrderBook.
        '''
        return self.order_list

class Trader:

    def __init__(self, trader_dict):
        '''
        Takes a Dictionary from a reponse and turns it into a Trader Object.
        '''
        self.id = int(trader_dict["id"])
        self.user = trader_dict["user"]
        self.cash = float(trader_dict["cash"])


    def get_dict(self):
        '''
        Converts the Trader Objects into a Dictionary.
        '''
        trader_dict = {
            "id": str(self.id),
            "name": self.name,
            "cash": str(self.cash)
        }
        return trader_dict

    def can_buy(self, order):
        '''
        Returns True if the Trader can purchase the order, False otherwise.
        '''
        return self.cash >= order.price * order.quantity
    def can_afford(self, price, quantity):
        '''
        Returns True if the Trader can afford the order, False otherwise.
        Duplicate function because we made a silly and are lazy.
        '''
        return self.cash >= price * quantity
    def can_sell(self, order):
        return True

