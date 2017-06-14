# testing online scheduling

import pool     # for pooling orders' requests
import order    # for instantiating orders
import scheduler# for finding the optimal order
import time     # for time testing
import sys      # for testing

# dict of orders (orders will be hashable)
orders = {}
# pool of preparations to be ordered and assigned
A = list()
# cooks in the kitchen. Each of them has its own work to do
# (which is assigned after the scheduler has run).
# Each cook has its own workload = total time it has to work
# (workload should be updated every time a cook finishes a
# dish, and as the time passes)
if len(sys.argv) > 1:
    # initialize scheduler from command line
    numberOfCooks = int(sys.argv[1])
    slownessMixing = 0.5
    if len(sys.argv) > 2:
        slownessMixing = float(sys.argv[2])
    scheduler.Scheduler.initialize(slownessMixing,[0]*numberOfCooks)

# an order arrive! (it arrives NOW!)
o1 = order.Order(["Pizza Margherita"],time.time())
o2 = order.Order(["Filet Mignon With Rich Balsamic Glaze"],
                time.time()+1)
# loads them in the pool
pool.inPool(o1,A,orders)
pool.inPool(o2,A,orders)
# optimize!
start_time = time.time()
# security code - avoids inputs that are too long!
c = "n"
if len(A) > 7:
    print "%i are too many dishes to test! are you sure??(y/n)"%(len(A))
    c = str(raw_input(">"))
if c=="y" or len(A) <= 7:
    best = scheduler.Scheduler.optimum(A,orders)
    print "done! in %f seconds"%(time.time()-start_time)
# DEBUG
for S in best:
    print 
    for i in S:
        print i
# flush
A = []
orders = {}
