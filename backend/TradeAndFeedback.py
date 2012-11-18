import PriceFeed
import Strategy
import time
import TradeBook
import json
import base64
import urllib
import urllib2
import httplib
import pycurl
import os


class TradeAndFeedback:
    def __init__(self):
        self.tb = TradeBook.TradeBook()
        self.all_strategy = Strategy.Strategy()
        self.serial = ''
        self.file = open("Result.json", "w")
        self.json_obj = {"team" : "RuntimeException", "destination" : "mcgillcodejam2012@gmail.com", "transactions" : []}
    
    def connect(self, ip, port):
        self.tb.connect(ip, port)
        
    def update_all(self, data, price_time):
        if('' == data):
            return
        self.all_strategy.update(float(data), price_time)
            
        if(self.all_strategy.check_SMA() == 1):
            self.tb.buy()
            price = self.tb.receive()
                
            if('E' == price):
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_SMA, "strategy" : "SMA"})
            else:
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_SMA, "strategy" : "SMA"})
            
        elif(self.all_strategy.check_SMA() == -1):
            self.tb.sell()
            price = self.tb.receive()
                
            if('E' == price):
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_SMA, "strategy" : "SMA"})
            else:
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_SMA, "strategy" : "SMA"})
            
        if(self.all_strategy.check_LWMA() == 1):
            self.tb.buy()
            price = self.tb.receive()
            if('E' == price):
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_LWMA, "strategy" : "LWMA"})
            else:
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_LWMA, "strategy" : "LWMA"})
        
        elif(self.all_strategy.check_LWMA() == -1):
            self.tb.sell()
            price = self.tb.receive()
                
            if('E' == price):
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_LWMA, "strategy" : "LWMA"})
            else:
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_LWMA, "strategy" : "LWMA"})
        
        if(self.all_strategy.check_EMA() == 1):
            self.tb.buy()
            price = self.tb.receive()
                
            if('E' == price):
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_EMA, "strategy" : "EMA"})
            else:
                self.json_obj["transactions"].append({"time" : str(price_time), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_EMA, "strategy" : "EMA"})
        
        elif(self.all_strategy.check_EMA() == -1):
            self.tb.sell()
            price = self.tb.receive()
                
            if('E' == price):
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_EMA, "strategy" : "EMA"})
            else:
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_EMA, "strategy" : "EMA"})
        
        if(self.all_strategy.check_TMA() == 1):
            self.tb.buy()
            price = self.tb.receive()
                
            if('E' == price):
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_TMA, "strategy" : "TMA"})
            else:
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "buy", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_TMA, "strategy" : "TMA"})
        
        elif(self.all_strategy.check_TMA() == -1):
            self.tb.sell()
            price = self.tb.receive()
                
            if('E' == price):
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_TMA, "strategy" : "TMA"})
            else:
                self.json_obj["transactions"].append({"time" : str(price_time + 1), "type" : "sell", "price" : data, 
                                                        "manager" : self.all_strategy.Manager_TMA, "strategy" : "TMA"})
    
    def post(self):
        os.system('''curl -X "POST" -H "Authorization: Basic Y29kZWphbTpBRkxpdGw0TEEyQWQx" -H "Content-Type:application/json" --data-binary @Result.json "https://stage-api.e-signlive.com/aws/rest/services/codejam"''')
        dict = self.tb.receive()
        self.serial = dict['ceremonyID']
    
    def write(self, obj):
        self.file.write(obj)
        self.file.flush()
        
    def json_write(self):
        self.write(json.dumps(self.json_obj, sort_keys = True, indent = 4))