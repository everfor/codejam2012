import Queue

class SMA:
    def __init__(self, period):
        self.N = period
        self.value_queue = Queue(maxsize = 0)
    def update(self, price, t):
        if(t <= 5):
            