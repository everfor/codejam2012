import PriceFeed
import Strategy
import time
import TradeBook
import json
import base64
import urllib
import httplib

class Test:
    def __init__(self):
        self.pf = PriceFeed.PriceFeed()
        self.tb = TradeBook.TradeBook()
        self.ip = '127.0.0.1'
        self.port1 = 8211
        self.port2 = 8212
        self.all_strategy = Strategy.Strategy()
        self.file = open("Result.json", "w")
        self.json_obj = {"team" : "RuntimeException", "destination" : "mcgillcodejam2012@gmail.com", "transactions" : []}
    
    def run(self):
        self.pf.connect(self.ip,self.port1)
        self.tb.connect(self.ip,self.port2)
        self.pf.startFeed()
        
        while(1):
            price_time, data = self.pf.getNextPrice()
            
            if(data == 'C'):
                #print data
                break 
            self.all_strategy.update(float(data), price_time)
            
            if(self.all_strategy.check_SMA() == 1):
                self.tb.buy()
                price = self.tb.receive()
                
                if('E' == price):
                    pass
                    #print 'ERROR:SMA buy ' + price + ' ' + self.all_strategy.Manager_SMA
                #print 'SMA buy ' + price + ' ' + self.all_strategy.Manager_SMA
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_SMA, "strategy" : "SMA"})
            
            elif(self.all_strategy.check_SMA() == -1):
                self.tb.sell()
                price = self.tb.receive()
                
                if('E' == price):
                    pass
                    #print 'ERROR: SMA sell ' + price + ' ' + self.all_strategy.Manager_SMA
                #print 'SMA sell ' + price + ' ' + self.all_strategy.Manager_SMA
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_SMA, "strategy" : "SMA"})
            
            if(self.all_strategy.check_LWMA() == 1):
                self.tb.buy()
                price = self.tb.receive()
                if('E' == price):
                    pass
                    #print 'ERROR: LWMA buy ' + price + ' ' + self.all_strategy.Manager_LWMA
                #print 'LWMA buy ' + price + ' ' + self.all_strategy.Manager_LWMA
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_LWMA, "strategy" : "LWMA"})
            elif(self.all_strategy.check_LWMA() == -1):
                self.tb.sell()
                price = self.tb.receive()
                
                if('E' == price):
                    pass
                    #print 'EEROR: LWMA sell ' + price + ' ' + self.all_strategy.Manager_LWMA
                #print 'LWMA sell ' + price + ' ' + self.all_strategy.Manager_LWMA
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_LWMA, "strategy" : "LWMA"})
            if(self.all_strategy.check_EMA() == 1):
                self.tb.buy()
                price = self.tb.receive()
                
                if('E' == price):
                    pass
                    #print 'ERROR: EMA buy ' + price + ' ' + self.all_strategy.Manager_EMA
                #print 'EMA buy ' + price + ' ' + self.all_strategy.Manager_EMA
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_EMA, "strategy" : "EMA"})
            elif(self.all_strategy.check_EMA() == -1):
                self.tb.sell()
                price = self.tb.receive()
                
                if('E' == price):
                    pass
                    #print 'ERROR: EMA sell ' + price + ' ' + self.all_strategy.Manager_EMA
                #print 'EMA sell ' + price + ' ' + self.all_strategy.Manager_EMA
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_EMA, "strategy" : "EMA"})
            if(self.all_strategy.check_TMA() == 1):
                self.tb.buy()
                price = self.tb.receive()
                
                if('E' == price):
                    pass
                    #print 'ERROR: TMA buy ' + price + ' ' + self.all_strategy.Manager_TMA
                #print 'TMA buy ' + price + ' ' + self.all_strategy.Manager_TMA
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_TMA, "strategy" : "TMA"})
            elif(self.all_strategy.check_TMA() == -1):
                self.tb.sell()
                price = self.tb.receive()
                
                if('E' == price):
                    pass
                    #print 'ERROR: EMA sell ' + price + ' ' + self.all_strategy.Manager_TMA
                #print 'EMA sell ' + price + ' ' + self.all_strategy.Manager_TMA
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_TMA, "strategy" : "TMA"})
        self.file.write(json.dumps(self.json_obj, sort_keys = True, indent = 4))
        self.post()
    
    def post(self):
        #temp = json.dumps(self.json_obj, sort_keys = True, indent = 4)
        params = urllib.urlencode(self.json_obj)
        auth = 'Y29kZWphbTpBRkxpdGw0TEEyQWQx'
        headers = {"Authorization": "Basic "+ auth, "Content-Type" : "application/json"}
        conn = httplib.HTTPConnection('https://stage-api.e-signlive.com/aws/rest/services/codejam:80')
        conn.request("POST", "", params, headers)
        response = conn.getresponse()
        print response.read().strip()
   
test = Test()
initial = time.time()
test.run()
print time.time() - initial