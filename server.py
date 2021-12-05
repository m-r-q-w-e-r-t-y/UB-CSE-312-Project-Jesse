import socketserver
import sys
import pymongo

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

    # Note: Takes request and processes a response
    def handle(self):
        data = self.request.recv(1024)

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
            data = ""
            while True:
                try:
                    # if self.request not in self.clients:
                    #     self.clients.append(self.request)
                    data = self.request.recv(1024)
                    webframe = bytearray(data)
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

    print("Listening on Port 8000 . . .")
    sys.stdout.flush()

    HOST, PORT = "0.0.0.0", 8000

    # Apply multithreading for webserver
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()