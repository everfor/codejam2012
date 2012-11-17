import socket
import DataBase as DB

class PriceFeed:
    def __init__(self):
        self.pr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Create a database:
        self.db = DB.DataBase()
    
    def connect(self, ip, port):
        #Connect to the server:
        self.pr_sock.connect((ip, port))
        print 'Connecting to ' + str(port)
    
    def startFeed(self):
        #Sned an "H" which means starting the communication:
        self.pr_sock.send('H\r\n')

        #Create a table:
        self.db.createTable()

        index=0
        price=''
        while(1):
            try:
                data = self.pr_sock.recv(1)
                #When it's a "C" all ends:
                if(data == 'C'):
                    break
                elif(data == '|'):
                    self.db.insertData(price)
                    price = ''
                    continue
                price += data
            except:
                print 'Exception occurred during the reception of data.'
        self.db.showValues() #Disable it after coding it all up.
