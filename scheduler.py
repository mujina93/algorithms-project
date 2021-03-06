# Scheduler - implementing my algorithm(s)
import sys  # for maxint
import time # for starting time of optimization
import copy

class Scheduler():
    # static variables for optimization
    numberOfCooks = 0
    bestMschedule = [[]]
    localCooksWorkloads = []
    localOrders = {}
    oldestOrderTime = 0
    # static variables used for optimization
    optimizationStartTime = 0
    # static variables used for cutting
    cuts = list()
    lowestLoss = sys.maxint
    # mixing constant. How much do you want to weigh
    # slowness with respect to coldness?
    # used for loss functions
    alpha = 0.5

    # initializer - sets number of cooks and their workloads,
    # sets the mixing constant alpha (=1 for only slowness)
    @classmethod
    def initialize(cls,alpha,WorkLoads):
        cls.alpha = alpha
        cls.localCooksWorkloads = WorkLoads
        cls.numberOfCooks = len(WorkLoads)
        cls.bestMschedule = [[]]*cls.numberOfCooks

    # given a pool of preparations, and a number of cooks M
    # returns the best M-schedule for the preparation
    @classmethod
    def optimum(cls,L,ords,optStartTime=time.time()):
        # variables setup
        cls.optimizationStartTime = optStartTime
        cls.localOrders = ords
        ordersTimes = list()
        for key in cls.localOrders:
            ordersTimes.append(cls.localOrders[key].get_timestamp())
        cls.oldestOrderTime = min(ordersTimes)
        # explore and find best schedule
        cls.generate(len(L),L)
        # prints output
        cls.explain()
        # flush
        del L[:]
        ords.clear()
        # returns best
        return cls.bestMschedule

    # Heap's algorithm for generating permutations of a list
    @classmethod
    def generate(cls,n,L):
        if n==1:
            # when a permutation is found, cut it in all
            # possible ways, and find the optimum schedule
            # among them. That will be stored into class static
            # variable bestMschedule
            cls.recursiveCut(1,L,cls.numberOfCooks)
        else:
            for i in range(n):
                cls.generate(n-1,L)
                if n%2==0:
                    L[i],L[n-1] = L[n-1],L[i]
                else:
                    L[0],L[n-1] = L[n-1],L[0]

    # algorithm for cutting the total schedule and assigning
    # pieces to the cooks
    # L = list to cut, M = n. of cooks
    # @classmethod
    # def cutRope(cls,L,M):
    #     # reset positions of the cuts:
    #     # the cuts from 1 to M-1 (the ones that will be
    #     # moved) at 0. The extremes: cuts[0] and cuts[N]
    #     # are fixed, one at 0, and one past the end of L.
    #
    #     # cut list in all possible ways and assign the pieces
    #     # to the cooks (put pieces in the Mschedule)
    #     cls.recursiveCut(1,L,M)

    # recursive part of cutter
    # !!! this calls the validation and loss function
    DrecursiveCut = False# DEBUGGER
    @classmethod
    def recursiveCut(cls,c,L,M):
        if c==1:
            cls.cuts = [0]*M +[len(L)]
        # moves current cut to previous cut's position
        cls.cuts[c] = cls.cuts[c-1]
        # do stuff until this cut has reached the end of L
        while cls.cuts[c] <= len(L):
            # creates empty M-schedule: a list (one for each cook)
            # of (each of them containing the dishes that we are
            # to assign to that cook)
            # e.g. Mschedule[0] is the list of new preparations that
            # could be assigned to the cook n.1
            Mschedule = list()
            for i in range(M):
                Mschedule.append(list())
            # let the cuts above move first
            if c < (M-1):
                cls.recursiveCut(c+1,L,M)
            # cut the list, and assign each piece
            for j in range(M):
                Mschedule[j] = L[cls.cuts[j]:cls.cuts[j+1]]
                # each dish is assigned its temporary cook
                # (this serves later to cls.validity() for
                # computing the tfinish in the right way)
                for dish in Mschedule[j]:
                    dish.set_temporaryCook(j)

            # check if the schedule violates contraints
            if cls.validity(Mschedule):
                # if valid, check if it's better than
                # the current best
                newLoss = cls.loss(Mschedule)
                if newLoss < cls.lowestLoss:
                    cls.bestMschedule = copy.deepcopy(Mschedule)
                    cls.lowestLoss = newLoss
            # advance the cut's position
            cls.cuts[c] += 1

    # Validity checker - checks if an Mschedule is valid
    Dvalidity = False # DEBUGGER
    @classmethod
    def validity(cls,MS):
        # # reset visited status of dishes
        # for S in MS:
        #     for i in S:
        #         i.set_visited(False)
        # for each cook (each schedule of the M-schedule)
        for C in range(cls.numberOfCooks):
            # and for each dish in the schedule
            for i in MS[C]:
                # if dish is final
                if i.is_final():
                    # if there is a violation in a tree
                    # then all the Mschedule is invalid
                    if cls.check(i,MS)==-1:
                        return False
        # if no violations were found, return True
        return True

    # Checker - for a single dish-Tree inside
    # an M-schedule
    # !!! sets dish as visited, and sets tfinish!
    Dcheck = False  # DEBUG
    @classmethod
    def check(cls,i,MS):
        # you are visiting the dish in the M-schedule
        i.set_visited(True)
        # set tfinish for the dish, adding the
        # workload of the cook number C, and the total
        # time of other dishes preceding this one
        # in the same schedule
        offsetSchedule = 0
        # total preparation time of other dishes
        # that have been assigned to be prepared before
        for p in MS[i.get_temporaryCook()]:
            if p == i:
                break
            else:
                offsetSchedule += p.get_T()

        offset = cls.localCooksWorkloads[i.get_temporaryCook()] +\
                                                offsetSchedule +\
                                        cls.optimizationStartTime

        i.set_tfinish(offset)

        for j in i.get_prerequisites():
            # check() returns False if there was
            # some violation, otherwise returns
            # the time
            tFinish_j = cls.check(j,MS)
            if tFinish_j==-1:
                # if there was a violation somewhere
                # in the tree, backpropagates the
                # information until the initial
                # call of check() returns False
                return -1
            else:
                # checks for violation: will j
                # be finised before i is started?
                if (tFinish_j > i.get_tstart()):
                    # VIOLATION
                    # the "violation error signal" starts
                    # backpropagating from here
                    return -1
        # if the dish has no prerequisites, or no violation
        # was found, return the tifinish of the dish
        return i.get_tfinish()

    # loss function(s)
    @classmethod
    def loss(cls,MS):
        return cls.alpha*cls.slowness(MS)+\
                (1-cls.alpha)*cls.coldness(MS)
    # slowness: upper bound on time of service.
    # all the customers which are currently at
    # the restaurant (and that have ordered)
    # will be served at most in a time = slowness
    @classmethod
    def slowness(cls,MS):
        slowestPrepTime = 0
        for S in MS:
            for i in S:
                if i.get_tfinish() > slowestPrepTime:
                    slowestPrepTime = i.get_tfinish()
        # returns Delta-time
        return slowestPrepTime - cls.oldestOrderTime
    # do the prepared dishes get cold?
    # yes, if the dishes for a single order
    # are spanned over a huge interval of time.
    @classmethod
    def coldness(cls,MS):
        for S in MS:
            for i in S:
                if i.get_tfinish() > cls.localOrders[i.get_ord()].get_max():
                    cls.localOrders[i.get_ord()].set_max(i.get_tfinish())
                elif i.get_tfinish() < cls.localOrders[i.get_ord()].get_min():
                    cls.localOrders[i.get_ord()].set_min(i.get_tfinish())
        worstRange = 0
        for key in cls.localOrders:
            r = cls.localOrders[key].get_range()
            if r > worstRange:
                worstRange = r
        return worstRange

    # Function that prints the result in a well formatted way
    @classmethod
    def explain(cls):
        print "Best M-schedule: (loss: ",
        print "%10.1f, slowness constant: %2.1f)"%(cls.lowestLoss,
                                                cls.alpha)
        form = lambda x: time.strftime("%H:%M",time.localtime(x))
        for C in range(cls.numberOfCooks):
            print "cook %i"%C
            for ind, dish in enumerate(cls.bestMschedule[C]):
                print " %i) from %s to %s: %s (ord. %s)"%(
                        ind,
                        form(dish.get_tstart()),
                        form(dish.get_tfinish()),
                        dish,
                        form(dish.get_ord()))
