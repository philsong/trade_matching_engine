"""
Alternetive Order Queue
which is Meant to be container of (Order)s
"""
import bintrees

class OrderQueue(object):
    """
    """
    def __init__(self):
        self.Orders = bintrees.FastRBTree()
        self.totalAmount = 0.0

    def append(self,order):
        k = order.timestamp
        self.Orders.insert(k,order)
        self.totalAmount += self.Orders[k].amount

    def count(self):
        return self.Orders.count

    def min_item(self):
        return self.Orders.min_item()

    def eat(self,amount):
        """
        use this only if amount <= self.amount
        return OrderToPop,RestAmount
        """
        current_amount = amount
        to_pop_orders = []
        while self.totalAmount>0 and current_amount>0:
            if not self.Orders or self.Orders.count==0:
                #print "amount:%.4f" % self.totalAmount
                self.totalAmount = 0.0
                return []

            min_item = self.Orders.min_item()
            min_i = min_item[1]
            # 1.enough
            # 2.not enough
            if min_i.amount <= current_amount:
                current_amount -= min_i.amount
                self.totalAmount -= min_i.amount
                to_pop_orders.append(self.Orders.pop_min()[1])
                continue
            # this is a hard case , need to take care of
            # first we split the order , take amount from current order
            # and make
            elif min_i.amount > current_amount:
                new_order = min_i.copy()
                new_order.amount = current_amount
                to_pop_orders.append(new_order)
                min_i.amount -= current_amount
                self.totalAmount -= current_amount
                current_amount = 0
                break
        # return:
        # 1.orders
        # 2.amount to trade
        # 3.amount left
        return to_pop_orders

    def remove(self,order):
        k = order.timestamp
        self.totalAmount -= self.Orders[k].amount
        self.Orders.remove(k)

    def get_price_depth(self):
        return self.totalAmount

    def is_empty(self):
        return self.Orders.count == 0
