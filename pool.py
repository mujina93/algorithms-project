import dish
import order

# functions that takes an order (object of type Order)
# and instantiates all the preparations that must be
# ordered/optimized and then preparated (the "pool")
def inPool(neworder,pool,orders):
    # add the new order to current orders
    orders[neworder.get_timestamp()] = neworder
    for r in neworder.get_requests():
        searchadd(r,pool,neworder.get_timestamp())

# function that does the dirty work
def searchadd(dishName,pool,orderID):
    # instatiate Dish object (actual dish to be prepared)
    # using a factory degisn pattern
    i = dish.Dish.factory(dishName,orderID)
    # add the dish to the pool
    pool.append(i)
    # search for its prerequisites,
    # instantiate them, and add them to the pool
    for j in i.recipe_prereq():
        # hooks dish j to i: j is an dish that
        # must be prepared before i in the schedule
        i.hook(searchadd(j,pool,orderID))
    # return object dish in order to be caught and to
    # be hooked by parent dish (that stores it as a
    # prerequisite)
    return i
