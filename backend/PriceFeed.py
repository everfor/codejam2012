import socket
import DataBase as DB

class PriceFeed:
    def __init__(self):
        self.pr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.time = 0
        self.data_list = []
    
    def connect(self, ip, port):
        #Connect to the server:
        self.pr_sock.connect((ip, port))
        print 'Connecting to ' + str(port)
        
    
    def startFeed(self):
        #Sned an "H" which means starting the communication:
        self.pr_sock.send('H\r\n')
     
    def getNextPrice(self):
        price = ''
        while(1):
            data = self.pr_sock.recv(1)
            #When it's a "C" all ends:
            if(data == 'C'):
                return -1, data
            elif(data == '|'):
                self.data_list.append(float(price))
                self.time += 1
                return self.time, price
            price += data
