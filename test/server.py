import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind(('', 8212))
#become a server socket
serversocket.listen(5)
print 'Listening'

conn, addr = serversocket.accept()

while(1):
    data = conn.recv(1024)
    print data

