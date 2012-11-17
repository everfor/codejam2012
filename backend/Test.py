import PriceFeed
import Strategy
import time
import TradeBook

class Test:
    def __init__(self):
        self.pf = PriceFeed.PriceFeed()
        self.tb = TradeBook.TradeBook()
        self.ip = '127.0.0.1'
        self.port1 = 8211
        self.port2 = 8212
        self.all_strategy = Strategy.Strategy()
        self.file = open("Result.txt", "w")
    def run(self):
        self.pf.connect(self.ip,self.port1)
        self.tb.connect(self.ip,self.port2)
        self.pf.startFeed()
        while(1):
            price_time, data = self.pf.getNextPrice()
            if(data == 'C'):
                print data
                break 
            self.all_strategy.update(float(data), price_time)
            if(self.all_strategy.check_SMA() == 1):
                #pass
                self.tb.buy()
                price = self.tb.receive()
                if('E' == price):
                    print 'ERROR:SMA buy ' + price + ' ' + self.all_strategy.Manager_SMA
                    self.file.write('ERROR:SMA buy ' + price + ' ' + self.all_strategy.Manager_SMA + '\n')
                    #print "Market closed"
                    #return
                print 'SMA buy ' + price + ' ' + self.all_strategy.Manager_SMA
                self.file.write('SMA buy ' + price + ' ' + self.all_strategy.Manager_SMA + '\n')
                #print 'SMA buy' + data
            elif(self.all_strategy.check_SMA() == -1):
                #pass
                self.tb.sell()
                price = self.tb.receive()
                if('E' == price):
                    print 'ERROR: SMA sell ' + price + ' ' + self.all_strategy.Manager_SMA
                    self.file.write('ERROR: SMA sell ' + price + ' ' + self.all_strategy.Manager_SMA + '\n')
                    #print "Market closed"
                    #return
                print 'SMA sell ' + price + ' ' + self.all_strategy.Manager_SMA
                self.file.write('SMA sell ' + price + ' ' + self.all_strategy.Manager_SMA + '\n')
                #print 'SMA sell' + data
            if(self.all_strategy.check_LWMA() == 1):
                #pass
                self.tb.buy()
                price = self.tb.receive()
                if('E' == price):
                    print 'ERROR: LWMA buy ' + price + ' ' + self.all_strategy.Manager_LWMA
                    self.file.write('ERROR: LWMA buy ' + price + ' ' + self.all_strategy.Manager_LWMA + '\n')
                    #print "Market closed"
                    #return
                print 'LWMA buy ' + price + ' ' + self.all_strategy.Manager_LWMA
                self.file.write('LWMA buy ' + price + ' ' + self.all_strategy.Manager_LWMA + '\n')
                #print 'LWMA buy' + data
            elif(self.all_strategy.check_LWMA() == -1):
                #pass
                self.tb.sell()
                price = self.tb.receive()
                if('E' == price):
                    print 'EEROR: LWMA sell ' + price + ' ' + self.all_strategy.Manager_LWMA
                    self.file.wirte('EEROR: LWMA sell ' + price + ' ' + self.all_strategy.Manager_LWMA + '\n')
                    #print "Market closed"
                    #return
                print 'LWMA sell ' + price + ' ' + self.all_strategy.Manager_LWMA
                self.file.write('LWMA sell ' + price + ' ' + self.all_strategy.Manager_LWMA + '\n')
                #print 'LWMA sell' + data
            if(self.all_strategy.check_EMA() == 1):
                #pass
                self.tb.buy()
                price = self.tb.receive()
                if('E' == price):
                    print 'ERROR: EMA buy ' + price + ' ' + self.all_strategy.Manager_EMA
                    self.file.write('ERROR: EMA buy ' + price + ' ' + self.all_strategy.Manager_EMA + '\n')
                    #print "Market closed"
                    #return
                print 'EMA buy ' + price + ' ' + self.all_strategy.Manager_EMA
                self.file.write('EMA buy ' + price + ' ' + self.all_strategy.Manager_EMA + '\n')
                #print 'EMA buy' + data
            elif(self.all_strategy.check_EMA() == -1):
                #pass
                self.tb.sell()
                price = self.tb.receive()
                if('E' == price):
                    print 'ERROR: EMA sell ' + price + ' ' + self.all_strategy.Manager_EMA
                    self.file.write('ERROR: EMA sell ' + price + ' ' + self.all_strategy.Manager_EMA + '\n')
                    #print "Market closed"
                    #return
                print 'EMA sell ' + price + ' ' + self.all_strategy.Manager_EMA
                self.file.write('EMA sell ' + price + ' ' + self.all_strategy.Manager_EMA + '\n')
                #print 'EMA sell' + data
            if(self.all_strategy.check_TMA() == 1):
                #pass
                self.tb.buy()
                price = self.tb.receive()
                if('E' == price):
                    print 'ERROR: TMA buy ' + price + ' ' + self.all_strategy.Manager_TMA
                    self.file.write('ERROR: TMA buy ' + price + ' ' + self.all_strategy.Manager_TMA + '\n')
                    #print "Market closed"
                    #return
                print 'TMA buy ' + price + ' ' + self.all_strategy.Manager_TMA
                self.file.write('TMA buy ' + price + ' ' + self.all_strategy.Manager_TMA + '\n')
                #print 'TMA buy' + data
            elif(self.all_strategy.check_TMA() == -1):
                #pass
                self.tb.sell()
                price = self.tb.receive()
                if('E' == price):
                    print 'ERROR: EMA sell ' + price + ' ' + self.all_strategy.Manager_TMA
                    self.file.write('ERROR: EMA sell ' + price + ' ' + self.all_strategy.Manager_TMA + '\n')
                    #print "Market closed"
                    #return
                print 'EMA sell ' + price + ' ' + self.all_strategy.Manager_TMA
                self.file.write('EMA sell ' + price + ' ' + self.all_strategy.Manager_TMA + '\n')
                #print 'EMA sell' + data
            
            #print data
        #print self.pf.data_list[0]
        
        
test = Test()
initial = time.time()
test.run()
print time.time() - initial