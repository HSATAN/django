#coding=utf-8
import socketserver
class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while 1:
            conn=self.request
            addr=self.client_address
            while 1:
                receiver_data=str(conn.recv(1024),encoding="utf8")
                print(receiver_data)
                if receiver_data=="bb":
                    conn.close()
                    break
                send_data=bytes(input(">>>>>>"),encoding="utf8")
                conn.sendall(send_data)

if __name__=="__main__":
    server=socketserver.ThreadingTCPServer(("localhost",8888),MyServer)
    server.serve_forever()