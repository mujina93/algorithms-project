# Class for one order of one table
# contains ordere dishes and timestamp as ID
import sys # for maxint

class Order:
    def __init__(self,requests,timestamp):
        self.requests = requests # strings with ordered dishes
        self.timestamp = timestamp # time of the order - UNIQUE
        # used by Scheduler, when computing coldness
        self.min = sys.maxint
        self.max = 0

    # getters
    def get_requests(self):
        return self.requests

    def get_timestamp(self):
        return self.timestamp

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_range(self):
        return self.max - self.min

    # setters
    def set_min(self,min):
        self.min = min

    def set_max(self,max):
        self.max = max

    # debugging
    def __str__(self):
        return "order-time:%i\nrequested:%s"%(
        self.timestamp, '\n'.join('{}: {}'.format(*k)
        for k in enumerate(self.requests)))
