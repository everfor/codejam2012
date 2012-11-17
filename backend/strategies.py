
def sum(t):
    i = 1
    summ = 0
    while(i <= t):
        summ += i
        i += 1
    return summ

class SMA:
    total = 0
    def __init__(self, period):
        self.N = period
        self.price_list = []
        self.value = 0
    def update(self, price, t):
        if(t <= self.N):
            self.price_list.append(price)
            self.total += price
            self.value = self.total / t
        else:
            self.value = self.value - self.price_list.pop(0) / self.N + price / self.N
            self.price_list.append(price)
    def showValue(self):
        return self.value
        
class LWMA:
    total = 0
    def __init__(self, period):
        self.N = period
        self.price_list = []
        self.value = 0
        self.divisor = sum(period)
        
    def update(self, price, t):
        if (t <= self.N):
            self.price_list.append(price)
            self.total += price * t
            self.value = self.total / sum(t)
        else:
            self.price_list.append(price)
            self.price_list.pop(0)
            i = 1
            self.total = 0
            for item in self.price_list:
                self.total += item * i
                i += 1
            self.value = self.total / self.divisor
     
    def showValue(self):
        return self.value
            
class EMA:
    def __init__(self, period):
        self.alpha = (float) (2.0 / (1.0 + period))
        self.value = 0
    def update(self, price, t):
        if(t == 1):
            self.value = price
        else:
            temp = self.value + self.alpha * (price - self.value)
            self.value = temp
    def showValue(self):
        return self.value
        
class TMA:
    total = 0
    def __init__(self, period):
        self.SMA_obj = SMA(period)
        self.N = period
        self.value = 0
        self.SMA_list = []
    def update(self, price, t):
        self.SMA_obj.update(price, t)
        self.SMA_list.append(self.SMA_obj.showValue())
        if(t <= self.N):
            self.total += self.SMA_obj.showValue()
            self.value = self.total / t
        else:
            self.total = 0
            self.SMA_list.pop(0)
            for item in self.SMA_list:
                self.total += item
            self.value = self.total / self.N
    def showValue(self):
        return self.value