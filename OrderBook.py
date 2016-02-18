"""
main code is from peatio
"""
import Queue
import OrderQueue

from bintrees import FastRBTree # An implementation of c/cython which is really fast

import Order
import time

class OrderBook(object):
    def __init__(self):
        self.book = [FastRBTree(),FastRBTree()] #sell and buy

    def submit(self,order):
        """
        I'd like to make a tree which is like {key:price,value:detail array} But WTF is detail array?
        """
        # type check
        #   inserting to orderbook  update the tree with {key:price  value:append to the Queue}
        order_type = order.order_type
        order_price = order.price
        if not self.book[order_type].get(order_price):
            self.book[order_type].insert(order_price,OrderQueue.OrderQueue())
            self.book[order_type][order_price].append(order)
        else:
            self.book[order_type][order_price].append(order)

    def cancel(self,order):
        order_type = order.order_type
        order_price = order.price
        if self.book[order_type].get(order_price):
            self.book[order_type][order_price].remove(order)
            #save some memory
            if self.book[order_type][order_price].is_empty():
                self.book[order_type].remove(order_price)
        else:
            pass

    def deal(self):
        """
        """
        min_sell,max_buy = self.closest_pair()
        deal_list_pool = []
        # if and only if
        if min_sell[0] <= max_buy[0]:
            sell_amount = min_sell[1].get_price_depth()
            buy_amount = max_buy[1].get_price_depth()
            # when eat the order,reduce  it`s amount
            if sell_amount != 0 and buy_amount != 0 and sell_amount >= buy_amount: #we should do
                sell_bills = min_sell[1].eat(buy_amount)
                buy_bills = max_buy[1].eat(buy_amount)
                #print "Ask %.2f/%.4f Bid %.2f/%.4f" % (min_sell[0],sell_amount,max_buy[0],buy_amount)
                deal_list_pool.append([sell_bills,buy_bills])
            else:
                #print "Ask %.2f/%.4f Bid %.2f/%.4f" % (min_sell[0],sell_amount,max_buy[0],buy_amount)
                sell_bills = min_sell[1].eat(sell_amount)
                buy_bills = max_buy[1].eat(sell_amount)
                deal_list_pool.append([sell_bills,buy_bills])
        # no matchable orders
        else:
            return False,deal_list_pool

        if self.book[0][min_sell[0]]:
            if self.book[0][min_sell[0]].is_empty() or min_sell[1].get_price_depth() == 0.0:
                if min_sell[1].get_price_depth() != 0.0: print "error:%.2f\n" % min_sell[0]
                self.book[0].remove(min_sell[0])

        if self.book[1][max_buy[0]]:
            if self.book[1][max_buy[0]].is_empty() or max_buy[1].get_price_depth() == 0.0:
                if max_buy[1].get_price_depth() != 0.0: print "error:%.2f\n" % max_buy[0]
                self.book[1].remove(max_buy[0])

        #self.print_deal_list(deal_list_pool)
        # deal_list_pool is an array of ask-bid pair
        return True,deal_list_pool

    def print_deal_list(self,l):
        for od_list in l:
            print od_list[0],od_list[1]

    def market_depth(self):
        ask_depth = []
        bid_depth = []

        for k,v in self.book[0].items():
            ask_depth.append((k,v.get_price_depth()))
        for k,v in self.book[1].items():
            bid_depth.append((k,v.get_price_depth()))

        return ask_depth,bid_depth

    def closest_pair(self):
        return self.book[0].min_item(),self.book[1].max_item()

"""
Other functions
"""
def make_random_market(N=10000):
    market = OrderBook()
    for i in range(N):
        market.submit(Order.gen_random_order())
    return market

def do_all_matches(market):
    for_start = time.time()

    status , order_list = market.deal()
    i = 0
    while status == True:
        i+=1
        status , order_list = market.deal()
        continue

    print "%d orders were processed.\n" % i

    wall_elapsed = (time.time() - for_start)
    wall_elapsed = wall_elapsed * 1000
    print "--for wall_elapsed  %.2f msecs," % (wall_elapsed)
    print "%.2f orders/sec" % (i/wall_elapsed*1000.)
    return i

