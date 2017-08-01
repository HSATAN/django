#coding=utf8
import socket
sock=socket.socket()
sock.connect(("localhost",8888))
while True:
    send_data=input(">>>>>>>")
    sock.sendall(bytes(send_data,encoding="utf8"))
    if send_data=="bb":
        break
    receive_data=str(sock.recv(1024),encoding="utf8")
    print(receive_data)
sock.close()