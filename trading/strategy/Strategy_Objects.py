

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

    def add_order(self, new_order):
        '''
        Adds a new order to the OrderBook if the order isn't in the OrderBook yet.
        new_order: new_order object.
        '''

        if not self.in_order_book(new_order):
            self.check_order_age(new_order)
            self.order_list.append(new_order)

    def get_oldest_order(self):
        '''
        Returns the oldest order in the OrderBook.
        '''
        return self.oldest_order



    def get_youngest_order(self):
        '''
        Returns the youngest order in the OrderBook.
        '''

        return self.youngest_order


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

