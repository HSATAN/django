#coding=utf8
import socketserver

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while 1:
            conn=self.request
            addr=self.client_address
            while True:
                data=str(conn.recv(1024),encoding="utf8")
                print(data)
                if data=="bb":
                    conn.close()
                    break
                conn.sendall(bytes(input(">>>>>>"),encoding="utf8"))

if __name__=="__main__":
    server=socketserver.ThreadingTCPServer(("localhost",8888),MyServer)
    server.serve_forever()
