# Scheduler - implementing my algorithm(s)

numberOfCooks = 2
# Heap's algorithm for generating permutations of a list
def generate(n,L):
    if n==1:
        Cutter.cutRope(L,numberOfCooks)
    else:
        for i in range(n):
            generate(n-1,L)
            if n%2==0:
                L[i],L[n-1] = L[n-1],L[i]
            else:
                L[0],L[n-1] = L[n-1],L[0]

# static class that provides the method for (recursively)
# cutting a given list
class Cutter():
    # static variables used by the class
    cuts = list()
    Mschedule = list()
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
            # advance the cut's position
            cls.cuts[c] += 1
