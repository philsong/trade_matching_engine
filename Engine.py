
import OrderBook
import time

if __name__ == '__main__':
    for_start = time.time()

    market = OrderBook.make_random_market()
    count = OrderBook.do_all_matches(market)

    wall_elapsed = (time.time() - for_start)
    wall_elapsed = wall_elapsed * 1000
    print "--__main__ wall_elapsed  %.2f msecs," % (wall_elapsed)
    print "%.2f orders/sec" % (count/wall_elapsed*1000.)