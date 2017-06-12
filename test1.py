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
# cooks in the kitchen. Each of them has its own work to do
# (which is assigned after the scheduler has run).
# Each cook has its own workload = total time it has to work
numberOfCooks = 2
cooksWorkloads = [0]*numberOfCooks
# two orders arrive!
o1 = order.Order(["Pizza Margherita", "Pizza Margherita"],
                        0)
o2 = order.Order(["Roast Chicken Red Whine Demi Glace Polenta"],
               1)
o3 = order.Order(["Ultimate Gourmet Grilled Cheese"],40)
# loads them in the pool
pool.inPool(o1,A,orders)
pool.inPool(o2,A,orders)
pool.inPool(o3,A,orders)
# optimize!
start_time = time.time()
# security code - avoids inputs that are too long!
c = "n"
if len(A) > 7:
    print "%i are too many dishes to test! are you sure??(y/n)"%(len(A))
    c = str(raw_input(">"))
if c=="y" or len(A) <= 7:
    best = scheduler.Scheduler.optimum(A,numberOfCooks,
                            cooksWorkloads,orders)
    print "done! in %f seconds"%(time.time()-start_time)
# flush
A = []
orders = {}
