import socket
import time

IP = '127.0.0.1'
PORT = 8212

pr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pr_sock.connect((IP, PORT))
print 'Connecting to ' + str(PORT)

while(1):
    input_s = raw_input('Send: ')
    print ord(input_s)
    pr_sock.send(input_s)
