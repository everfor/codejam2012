import socket
import DataBase as DB

IP = '127.0.0.1'
PORT = 8211

class PriceFeed:
    pr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        #Create a database:
        self.db = DB.DataBase()
    
    def connect(self):
        #Connect to the server:
        self.pr_sock.connect((IP, PORT))
        print 'Connecting to ' + str(PORT)
    
    def startFeed(self):
        #Sned an "H" which means starting the communication:
        self.pr_sock.send('H\r\n')

        #Create a table:
        self.db.createTable()

        index=0
        price=''
        while(1):
            try:
                data = pr_sock.recv(1)
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
