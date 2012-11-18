import strategies as S

class Strategy:
    Delta1_SMA = 0
    Delta2_SMA = 0
    Delta1_LWMA = 0
    Delta2_LWMA = 0
    Delta1_LWMA = 0
    Delta2_LWMA = 0
    Delta1_EMA = 0
    Delta2_EMA = 0
    Delta1_TMA = 0
    Delta2_TMA = 0
    def __init__(self):
        self.SMA_fast = S.SMA(5)
        self.SMA_slow = S.SMA(20)
        self.Manager_SMA = 'Manager1'
        
        self.LWMA_fast = S.LWMA(5)
        self.LWMA_slow = S.LWMA(20)
        self.Manager_LWMA = 'Manager1'
        
        self.EMA_fast = S.EMA(5)
        self.EMA_slow = S.EMA(20)
        self.Manager_EMA = 'Manager2'
        
        self.TMA_fast = S.TMA(5)
        self.TMA_slow = S.TMA(20)
        self.Manager_TMA = 'Manager2'
        
    def update(self, price, t):
        if(t == 1):
            self.SMA_fast.update(price, t)
            self.SMA_slow.update(price, t)
            self.LWMA_fast.update(price, t)
            self.LWMA_slow.update(price, t)
            self.EMA_fast.update(price, t)
            self.EMA_slow.update(price, t)
            self.TMA_fast.update(price, t)
            self.TMA_slow.update(price, t)
            self.Delta1_SMA = self.SMA_fast.showValue() - self.SMA_slow.showValue()
            self.Delta1_LWMA = self.LWMA_fast.showValue() - self.LWMA_slow.showValue()
            self.Delta1_EMA = self.EMA_fast.showValue() - self.EMA_slow.showValue()
            self.Delta1_TMA = self.TMA_fast.showValue() - self.TMA_slow.showValue()
            return
        else:
            self.Delta1_SMA = self.Delta2_SMA
            self.Delta1_LWMA = self.Delta2_LWMA
            self.Delta1_EMA = self.Delta2_EMA
            self.Delta1_TMA = self.Delta2_TMA
            self.SMA_fast.update(price, t)
            self.SMA_slow.update(price, t)
            self.LWMA_fast.update(price, t)
            self.LWMA_slow.update(price, t)
            self.EMA_fast.update(price, t)
            self.EMA_slow.update(price, t)
            self.TMA_fast.update(price, t)
            self.TMA_slow.update(price, t)
            self.Delta2_SMA = self.SMA_fast.showValue() - self.SMA_slow.showValue()
            self.Delta2_LWMA = self.LWMA_fast.showValue() - self.LWMA_slow.showValue()
            self.Delta2_EMA = self.EMA_fast.showValue() - self.EMA_slow.showValue()
            self.Delta2_TMA = self.TMA_fast.showValue() - self.TMA_slow.showValue()
            if(t == 5401):
                self.Manager_EMA = 'Manager3'
                self.Manager_TMA = 'Manager3'
                return
            if(t == 7201):
                self.Manager_SMA = 'Manager4'
                self.Manager_LWMA = 'Manager4'
                return
            if(t == 12601):
                self.Manager_EMA = 'Manager5'
                self.Manager_TMA = 'Manager5'
                return
            if(t == 14401):
                self.Manager_SMA = 'Manager3'
                self.Manager_LWMA = 'Manager3'
                return
            if(t == 16201):
                self.Manager_SMA = 'Manager5'
                self.Manager_LWMA = 'Manager5'
                self.Manager_EMA = 'Manager4'
                self.Manager_TMA = 'Manager4'
                return
            if(t == 19801):
                self.Manager_SMA = 'Manager6'
                self.Manager_LWMA = 'Manager6'
                return
            if(t == 21601):
                self.Manager_EMA = 'Manager5'
                self.Manager_TMA = 'Manager5'
                return
            if(t == 27001):
                self.Manager_SMA = 'Manager7'
                self.Manager_LWMA = 'Manager7'
                return
            if(t == 28801):
                self.Manager_EMA = 'Manager6'
                self.Manager_TMA = 'Manager6'
                return
            
    def check_SMA(self):
        if(self.Delta1_SMA < 0 and self.Delta2_SMA >= 0):
            return 1
        elif(self.Delta1_SMA > 0 and self.Delta2_SMA <= 0):
            return -1
        return 0
        
    def check_LWMA(self):
        if(self.Delta1_LWMA <0 and self.Delta2_LWMA >= 0):
            return 1
        elif(self.Delta1_LWMA > 0 and self.Delta2_LWMA <= 0):
            return -1
        return 0
        
    def check_EMA(self):
        if(self.Delta1_EMA <0 and self.Delta2_EMA >= 0):
            return 1
        elif(self.Delta1_EMA > 0 and self.Delta2_EMA <=0):
            return -1
        return 0
        
    def check_TMA(self):
        if(self.Delta1_TMA <0 and self.Delta2_TMA >= 0):
            return 1
        elif(self.Delta1_TMA > 0 and self.Delta2_TMA <=0):
            return -1
        return 0