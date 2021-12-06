import socketserver
import sys
from Request import Request
from WebSocket import WebSocket
from routes.Route import Route
from routes.Routes import routes

# Note: Handles TCP connections (request and response)
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # HTTP
        request = Request(self)

        if Route.fileRequested(request):
            response = Route.getFileDynamically(request)
            return self.request.sendall(response)
        
        for route in routes:
            if route.match(request):
                response = route.getResponse(request)
                return self.request.sendall(response)

        # TODO: Return 404 if no routes match

        # Websocket
        if "Upgrade" in request.headers and request.headers["Upgrade"] == "websocket":
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