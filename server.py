import socketserver
import sys
import pymongo
import math
from Response import Response
from Request import Request
from WebSocket import WebSocket
from pprint import pprint
from FormParser import formParser


# Note: Handles TCP connections (request and response)
class MyTCPHandler(socketserver.BaseRequestHandler):

    clients = []
    counter = 0
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["database"]
    info = db["clients"]

    def handle(self):

        data = self.request.recv(1024)

        # HTTP
        request = Request(data)

        if "Content-Length" in request.getHeaders() and "Content-Type" in request.getHeaders() and "multipart/form-data" in request.getHeaders()["Content-Type"]:
            bytes_needed = int(request.getHeaders()["Content-Length"])
            bytes_received = len(data) - len(data.split(b'\r\n\r\n')[0])
            while bytes_received < bytes_needed:
                buffer_chunk = self.request.recv(1024)
                if not buffer_chunk:
                    break
                data += buffer_chunk
                bytes_received += len(buffer_chunk)
            form = formParser(data)
            request = Request(data)
        response = Response(request, self.info)
        self.request.sendall(response.getResponse())

        # Websocket
        if "Upgrade" in request.getHeaders() and request.getHeaders()["Upgrade"] == "websocket":
            print("---------------- WebSocket Zone ----------------")
            request = ""
            while True:
                try:
                    # if self.request not in self.clients:
                    #     self.clients.append(self.request)
                    request = self.request.recv(1024)
                    webframe = bytearray(request)
                    websocket = WebSocket(webframe)
                    self.request.sendall(websocket.getResponse())
                    # for c in self.clients:
                    #     c.sendall(websocket.getResponse())
                except:
                    break
            print("------------------------------------------------")

        print("-------")

if __name__ == "__main__":  
    print("\n")

    print("Listening on Port 8080 . . .")
    sys.stdout.flush()

    HOST, PORT = "0.0.0.0", 8000

    # Apply multithreading for webserver
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()