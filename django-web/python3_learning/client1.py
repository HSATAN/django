#coding

import socket
s=socket.socket()
s.connect(("localhost",8888))
while 1:
    s.sendall(bytes(input(">>>>>>"),encoding="utf8"))
    data=str(s.recv(1024),encoding="utf8")
    print(len(data))
    print(data)
