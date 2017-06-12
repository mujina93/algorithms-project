# Dish object(s). Each of them represents a "unit" that
# can be prepared. The instantiation is done via factory
# design pattern.
class Dish:
    # Create based on class name:
    # constructor called through the dictionary Recipes
    # that contains all class names
    def factory(type,order):
        return Recipes[type](order)
    factory = staticmethod(factory)

    # contruct the Dish object assigning it to the order
    # to which it belongs
    def __init__(self,order):
        self.ord = order
        self.prerequisites = list()
        self.recipePrerequisites = []
        self.visited = False
        self.tfinish = 0

    # hook to a new prerequisite (considered as child
    # or neighbour)
    def hook(self,other):
        self.prerequisites.append(other)

    # returns recipe names (just names!) of the
    # prerequisites of this dish
    def recipe_prereq(self):
        return self.recipePrerequisites

    # check if the dish is simple (has no prerequisites for
    # being prepared)
    def is_simple(self):
        if len(self.recipePrerequisites)==0:
            return True
        else:
            return False

    # gets prerequisites (actual ordered dishes, which
    # are instantiated objects, hooked to this dish as children)
    def get_prerequisites(self):
        return self.prerequisites

    # get preparation time
    # each subclass initialize its own prep time
    def get_T(self):
        return self.T

    # get order to which the preparation is assigned
    def get_ord(self):
        return self.ord

    # was the dish visited by the optimizer?
    def was_visited(self):
        return self.visited

    # setter
    def set_visited(self, logic):
        self.visited = logic

    # updater for tfinish. The scheduler updates from the
    # outside the tifinish for the dish, based on the
    # information of: which cook (with its workload) was
    # the dish assigned?
    def set_tfinish(self, workload):
        # the time at which the dish will be finished is:
        # = time for preparing it
        # + time at which the order was made
        # + time that has to pass until the assigned cook
        # is free to cook that dish
        self.tfinish = self.T + self.ord + workload

    # getter for tfinish
    def get_tfinish(self):
        return self.tfinish

    # getter for tstart
    def get_tstart(self):
        return self.tfinish - self.T

    # debugging
    def __str__(self):
        return self.__class__.__name__

# Dishes classes - RECIPE BOOK
# using a static variable for recipe_prerequisites
# (names of dishes that serve for cookin that one)
class RoastChickenRedWhineDemiGlacePolenta(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 10
        self.recipePrerequisites = ["Roast Chicken","Polenta"]
class RoastChicken(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 40
class Polenta(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 10
class CrispyFishTacosWithSpicyYogurtSauce(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 7
        self.recipePrerequisites = \
            ["Crispy Fish","Tacos","Yogurt Sauce"]
class CrispyFish(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 5
        self.recipePrerequisites = ["Cleaned Fish"]
class CleanedFish(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 2
class Tacos(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=4
class YogurtSauce(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=1
class UltimateGourmetGrilledCheese(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=6
class PizzaMargherita(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=14

# Recipes dictionary, used by the factory to build objects
Recipes = {
    ###
    "Roast Chicken Red Whine Demi Glace Polenta":RoastChickenRedWhineDemiGlacePolenta,
    "Roast Chicken":RoastChicken,
    "Polenta":Polenta,
    ###
    "Crispy Fish Tacos With Spicy Yogurt Sauce":CrispyFishTacosWithSpicyYogurtSauce,
    "Crispy Fish":CrispyFish,
    "Cleaned Fish":CleanedFish,
    "Tacos":Tacos,
    "Yogurt Sauce":YogurtSauce,
    ###
    "Ultimate Gourmet Grilled Cheese":UltimateGourmetGrilledCheese,
    ###
    "Pizza Margherita":PizzaMargherita
}
