import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('142.157.168.122',8211))
sock.send('H\r\n')

while(1):
    data=sock.recv(1024)
    print data,
