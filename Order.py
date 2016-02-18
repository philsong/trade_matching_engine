"""
From peatio

"""
import copy # for order split

class Order(object):
    """
    Order class to be store in the ask/bid RBTree value field
    """
    def __init__(self,id,timestamp,order_type,price,amount,Market):
        """
        id may be Uid
        timestamp is when submit
        order_type is 0 or 1 corresponse to sell or buy
        price is a float round to 0.01
        Market is initial BTC or LTC
        """
        self.id = id
        self.timestamp = timestamp
        self.order_type = order_type
        self.price = round(price,2)
        self.amount = round(amount,4)
        self.Market = Market

    def __cmp__(self,other):
        if self.price < other.price:
            return -1
        elif self.price == other.price:
            if self.timestamp <= other.timestamp:
                return -1
            else:
                return 1
        else:
            return 1 # We should not consider them as the same orders

    def copy(self):
        copy_order = Order(self.id,
                           self.timestamp,
                           self.order_type,
                           self.price,
                           self.amount,
                           self.Market)
        return copy_order
#    def __eq__(self,other):
#        self.id == other.id

#    def __str__(self):
#        return "price:%s id:%d" % (self.price,self.id)

#    def __coerce__(self):
#        pass

######################################################
#
#
def gen_random_order():
    import time
    import numpy as np
    return Order(np.random.randint(100000),
                 time.time(),
                 np.random.randint(2),
                 3000+100*np.random.randn(),
                 abs(np.random.randn()),
                 "BTC")
