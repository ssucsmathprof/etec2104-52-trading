

class OrderBook:
    def __init__(self, order_list):
        self.order_list = order_list

    def add_order(self, new_order):
        self.order_list.append(new_order)

    def get_oldest_order(self):
        oldest_order = None
        for order in self.order_list:
            if oldest_order is None or order.created_at < oldest_order.created_at:
                oldest_order = order

        return oldest_order

    def in_order_book(self, check_order):
        if len(self.order_list) == 0:
            return False

        for in_order in self.order_list:
            if in_order == check_order:
                return True
        return False

    def get_all_orders(self):
        return self.order_list

    def get_youngest_order(self):
        youngest_order = None
        for order in self.order_list:
            if youngest_order is None or order.created_at > youngest_order.created_at:
                youngest_order = order
        return youngest_order
