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
o1 = order.Order(["Roast Chicken Red Whine Demi Glace Polenta",
                    "Pizza Margherita",
                    "Pizza Margherita"],
                        0000)
o2 = order.Order(["Crispy Fish Tacos With Spicy Yogurt Sauce",
                    "Ultimate Gourmet Grilled Chicken"],
               0001)
# loads them in the pool
pool.inPool(o1,A,orders)
pool.inPool(o2,A,orders)
# optimize!
start_time = time.time()
scheduler.generate(len(A),A)
print "done! in %f seconds"%(time.time()-start_time)
