import socket
import time

IP = '127.0.0.1'
PORT = 8211

pr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pr_sock.connect((IP, PORT))
print 'Connecting to ' + str(PORT)
pr_sock.send('H\r\n')
print 'Sent H'

while 1:
    data = pr_sock.recv(7)

    print data
