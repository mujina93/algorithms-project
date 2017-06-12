# Class for one order of one table
# contains ordere dishes and timestamp as ID
class Order:
    def __init__(self,requests,timestamp):
        self.requests = requests # strings with ordered dishes
        self.timestamp = timestamp # time of the order - UNIQUE

    # getters
    def get_requests(self):
        return self.requests

    def get_timestamp(self):
        return self.timestamp

    # debugging
    def __str__(self):
        return "order-time:%i\nrequested:%s"%(
        self.timestamp, '\n'.join('{}: {}'.format(*k)
        for k in enumerate(self.requests)))
