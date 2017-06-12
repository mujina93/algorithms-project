# New recipetest
# trying Dish, Order, Pool
import pool     # for pooling orders' requests
import order    # for instantiating orders
import scheduler# for finding the optimal order
import time     # for time testing

# dict of orders (orders will be hashable)
orders = {}
# pool of preparations to be ordered and assigned
A = list()
# two orders arrive!
o1 = order.Order(["Roast Chicken Red Whine Demi Glace Polenta"],
                        0000)
o2 = order.Order(["Crispy Fish Tacos With Spicy Yogurt Sauce"],
               0001)
# loads them in the pool
pool.inPool(o1,A,orders)
pool.inPool(o2,A,orders)
# optimize!
start_time = time.time()
# security code - avoids inputs that are too long!
c = "n"
if len(A) > 8:
    print "%i are too many dishes to test! are you sure??(y/n)"%(len(A))
    c = str(raw_input(">"))
if c=="y" or len(A) <= 8:
    scheduler.generate(len(A),A)
    print "done! in %f seconds"%(time.time()-start_time)
