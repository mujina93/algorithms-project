# Dish object(s). Each of them represents a "unit" that
# can be prepared. The instantiation is done via factory
# design pattern.

#import copy # for instantiating new local variables

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
        self.final = False
        self.temporaryCook = -1

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
    def set_tfinish(self, offset):
        # the time at which the dish will be finished is:
        # = current time
        # + offset (= workload of the cook that should
        # prepare it + preparation times of new dishes
        # assigned to that cook BEFORE this dish
        # + time at which the scheduler has started running)
        # is free to cook that dish
        self.tfinish = self.T  + offset

    # getter for tfinish
    def get_tfinish(self):
        return self.tfinish

    # getter for tstart
    def get_tstart(self):
        return self.tfinish - self.T

    # is it a final dish? (not an intermediate step)
    # final dishes are the ones that appear on menu and
    # that can be ordered
    def is_final(self):
        return self.final

    # temporary cook getter/setter. Temporary cook is set
    # by the scheduler. This information is retrieved when
    # computing the tfinish time for a dish (you must know)
    # which coooks were the prerequisites of this dish
    # assigned to, in order to compute possible violations
    def set_temporaryCook(self, index):
        self.temporaryCook = index

    def get_temporaryCook(self):
        return self.temporaryCook

    # debugging
    def __str__(self):
        finalStar = ""
        if self.final:
            finalStar = '*'
        return self.__class__.__name__ + finalStar

# Dishes classes - RECIPE BOOK
# using a static variable for recipe_prerequisites
# (names of dishes that serve for cookin that one)
class RoastChickenRedWhineDemiGlacePolenta(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 10*60
        self.recipePrerequisites = ["Roast Chicken","Polenta"]
        self.final = True
class RoastChicken(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 40*60
class Polenta(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 10*60
class CrispyFishTacosWithSpicyYogurtSauce(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 7*60
        self.recipePrerequisites = \
            ["Crispy Fish","Tacos","Yogurt Sauce"]
        self.final = True
class CrispyFish(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 5*60
        self.recipePrerequisites = ["Cleaned Fish"]
class CleanedFish(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T = 2*60
class Tacos(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=4*60
class YogurtSauce(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=1*60
class UltimateGourmetGrilledCheese(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=6*60
        self.final = True
class PizzaMargherita(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=14*60
        self.final = True
class PizzaDiavola(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=15*60
        self.final = True
class FiletMignonWithRichBalsamicGlaze(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=15*60
        self.final = True
        self.recipePrerequisites = ["Filet Mignon"]
class FiletMignon(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=5*60
class MisoSoup(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=6*60
        self.final=True
class Sashimi(Dish):
    def __init__(self,order):
        Dish.__init__(self,order)
        self.T=5*60
        self.final=True

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
    "Pizza Margherita":PizzaMargherita,
    ###
    "Pizza Diavola":PizzaDiavola,
    ###
    "Miso Soup":MisoSoup,
    ###
    "Sashimi":Sashimi,
    ###
    "Filet Mignon With Rich Balsamic Glaze":FiletMignonWithRichBalsamicGlaze,
    "Filet Mignon":FiletMignon
}
