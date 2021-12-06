import socketserver
import sys
import pymongo
import math
from Response import Response
from Request import Request
from WebSocket import WebSocket
from pprint import pprint


# Note: Handles TCP connections (request and response)
class MyTCPHandler(socketserver.BaseRequestHandler):

    clients = []
    counter = 0
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["database"]
    info = db["clients"]

    def handle(self):
        all_request = []

        data = self.request.recv(1024)

        if b'Content-Type' in data:
            content_length = ''

            splitRequest = data.splitlines()

            for i in splitRequest:
                if 'Content-Length' in i.decode('utf-8'):
                    content_length += i.decode('utf-8')

            content_length = content_length.split(' ')[1]

            for i in range(0, math.ceil(int(content_length) / 1024)):
                all_request.append(self.request.recv(1024))

            data += b''.join(all_request)

        print("Request\n-----------------------------------")
        print(data)
        print("-----------------------------------")

        # HTTP
        request = Request(data)
        response = Response(request, self.info)
        self.request.sendall(response.getResponse())
        print(request.toString())
        sys.stdout.flush()
        print(response.toString())
        sys.stdout.flush()

        # if self.info.count_documents(response.returnUser()) == 0:
        #         self.info.insert_one(returnUser)

        # print("Mongo")
        # collection = self.info.find({})
        # for document in collection:
        #     pprint(document)


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