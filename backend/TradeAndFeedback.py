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
import subprocess


class TradeAndFeedback:
    def __init__(self):
        self.tb = TradeBook.TradeBook()
        self.all_strategy = Strategy.Strategy()
        self.cere = ''
        self.file = open("Result.json", "w")
        self.hisfile = open("History.txt", "w")
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
        proc = subprocess.Popen('''curl -X "POST" -H "Authorization: Basic Y29kZWphbTpBRkxpdGw0TEEyQWQx" -H "Content-Type:application/json" --data-binary 
                                @Result.json "https://stage-api.e-signlive.com/aws/rest/services/codejam"''', 
                                shell = True,
                                stdout = subprocess.PIPE
                                )
        self.cere = proc.stdout.read()[15:-2]
    
    def write(self, obj):
        self.file.write(obj)
        self.file.flush()
        
    def json_write(self):
        self.write(json.dumps(self.json_obj, sort_keys = True, indent = 4))
        
    def history(self):
        self.hisfile.write("Time            Price           Type" + '\n')
        for transaction in self.json_obj['transactions']:
            self.hisfile.write(transaction['time'] + "              " + transaction['price'] + "            " + transaction['type'] + '\n')
        self.hisfile.close()