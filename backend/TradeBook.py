import socket

class TradeBook:
    def __init__(self):
        self.pr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self, ip, port):
        #Connect to the server:
        self.pr_sock.connect((ip, port))
        return
    
    def buy(self):
       self.pr_sock.send('B\r\n')
       return
       
    def sell(self):
       self.pr_sock.send('S\r\n')
       return
       
    def receive(self):
        return self.pr_sock.recv(7)