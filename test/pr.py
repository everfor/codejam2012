import socket
import time
import sqlite3 as sqlite
import sys
import time
import DataBase as DB

IP = '127.0.0.1'
PORT = 8211

pr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Create a database:
db = DB.DataBase()

#Connect to the server:
pr_sock.connect((IP, PORT))
print 'Connecting to ' + str(PORT)

#Sned an "H" which means starting the communication:
pr_sock.send('H\r\n')

#Create a table:
db.createTable()

index=0
price=''
initial=time.time()
while(1):
    try:
        data = pr_sock.recv(1)
        #When it's a "C" all ends:
        if(data == 'C'):
            break
        elif(data == '|'):
            db.insertData(price)
            price = ''
            continue
        price += data
    except:
        print 'Exception occurred during the reception of data.'
db.showValues()
delta_time = time.time() - initial
print delta_time