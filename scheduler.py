# Scheduler - implementing my algorithm(s)
import sys # for maxint

class Scheduler():
    # static variables for partial results
    numberOfCooks = 0
    bestMschedule = [[]]
    localCooksWorkloads = []
    localOrders = {}
    # static variables used for cutting
    cuts = list()
    Mschedule = list()
    lowestLoss = sys.maxint
    # mixing constant. How much do you want to weigh
    # slowness with respect to coldness?
    # used for loss functions
    alpha = 0.5

    # given a pool of preparations, and a number of cooks M
    # returns the best M-schedule for the preparation
    @classmethod
    def optimum(cls,L,M,WL,ords):
        cls.localCooksWorkloads = WL
        cls.numberOfCooks = M
        cls.localOrders = ords
        cls.generate(len(L),L)
        # DEBUG
        cls.explain()
        return cls.bestMschedule

    # Heap's algorithm for generating permutations of a list
    @classmethod
    def generate(cls,n,L):
        if n==1:
            # when a permutation is found, cut it in all
            # possible ways, and find the optimum schedule
            # among them. That will be stored into class static
            # variable bestMschedule
            cls.cutRope(L,cls.numberOfCooks)
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
    @classmethod
    def cutRope(cls,L,M):
        # reset positions of the cuts:
        # the cuts from 1 to M-1 (the ones that will be
        # moved) at 0. The extremes: cuts[0] and cuts[N]
        # are fixed, one at 0, and one past the end of L.
        cls.cuts = [0]*M +[len(L)]
        # empties M-schedule: a list (one for each cook)
        # of (each of them containing the dishes that we are
        # to assign to that cook)
        # e.g. Mschedule[0] is the list of new preparations that
        # could be assigned to the cook n.1
        for i in range(M):
            cls.Mschedule.append(list())
        # cut list in all possible ways and assign the pieces
        # to the cooks (put pieces in the Mschedule)
        cls.recursiveCut(1,L,M)

    # recursive part of cutter
    @classmethod
    def recursiveCut(cls,c,L,M):
        # moves current cut to previous cut's position
        cls.cuts[c] = cls.cuts[c-1]
        # do stuff until this cut has reached the end of L
        while cls.cuts[c] < len(L):
            # let the cuts above move first
            if c < (M-1):
                recursiveCut(c+1,L,M)
            else:
                # cut the list, and assign each piece
                for j in range(M):
                    cls.Mschedule[j] =\
                        L[cls.cuts[j]:cls.cuts[j+1]]
                    # DEBUG
                    # print " cook %i:"%j
                    # print "%s"%'  \n'.join('{}: {}'.format(*k)
                    #     for k in enumerate(cls.Mschedule[j]))
                # check if the schedule violates contraints
                if cls.validity(cls.Mschedule):
                    # if valid, check if it's better than
                    # the current best
                    newLoss = cls.loss(cls.Mschedule)
                    if newLoss < cls.lowestLoss:
                        cls.bestMschedule = cls.Mschedule
                        cls.lowestLoss = newLoss
            # advance the cut's position
            cls.cuts[c] += 1

    # Validity checker - checks if an Mschedule is valid
    @classmethod
    def validity(cls, MS):
        # for each cook (each schedule of the M-schedule)
        for C in range(cls.numberOfCooks):
            # and for each dish in the schedule
            for i in MS[C]:
                # if dish wasn't visited yet
                if i.was_visited()==False:
                    # if there is a violation in a tree
                    # then all the Mschedule is invalid
                    if cls.check(i,C)==False:
                        return False
        # reset visited status of dishes
        for S in MS:
            for i in S:
                i.set_visited(False)
        # if no violations were found, return True
        return True

    # Checker - for a single dish-Tree inside
    # an M-schedule
    # !!! sets dish as visited, and sets tfinish!
    @classmethod
    def check(cls,i,cook):
        # you are visiting the dish in the M-schedule
        i.set_visited(True)
        # set tfinish for the dish, adding the
        # workload of the cook number C
        i.set_tfinish(cls.localCooksWorkloads[cook])
        for j in i.get_prerequisites():
            # check() returns False if there was
            # some violation, otherwise returns
            # the time
            tFinish_j = cls.check(j,cook)
            if tFinish_j==False:
                # if there was a violation somewhere
                # in the tree, backpropagates the
                # information until the initial
                # call of check() returns False
                return False
            else:
                # checks for violation: will j
                # be finised before i is started?
                if tFinish_j > i.get_tstart():
                    # VIOLATION
                    return False
                else:
                    # ok
                    return i.get_tfinish()

    # loss function(s)
    @classmethod
    def loss(cls,MS):
        return cls.alpha*cls.slowness(MS)+\
                (1-cls.alpha)*cls.coldness(MS)
    # slowness: upper bound on time of service.
    # all the customers which are currently at
    # the restaurant (and that have ordered)
    # will be served at most at time = slowness
    @classmethod
    def slowness(cls,MS):
        slowestPrepTime = 0
        for S in MS:
            for i in S:
                if i.get_tfinish() > slowestPrepTime:
                    slowestPrepTime = i.get_tfinish()
        return slowestPrepTime
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
        print "Best M-schedule: (loss: %f)"%cls.lowestLoss
        for C in range(cls.numberOfCooks):
            print "cook %i"%C
            print ' \n'.join('{}: {}'.format(*k)
                    for k in enumerate(cls.bestMschedule[C]))
