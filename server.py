import socketserver
from Request import Request
from websocket.WebSocketHandler import WebSocketHandler
from websocket.WebSocketParser import WebSocketParser
from routes.Route import Route
from routes.Routes import routes
from db_init import User
from clientManager_init import Manager

# Note: Handles TCP connections (request and response)
from routes.utility_functions import isAuthenticated


class MyTCPHandler(socketserver.BaseRequestHandler):
    currentUser = None

    def handle(self):
        data = self.request.recv(1024)

        # HTTP
        request = Request(data,self)
        print(f'{request.req_type} {request.path}')

        if Route.fileRequested(request):
            response = Route.getFileDynamically(request)
            return self.request.sendall(response)

        for route in routes:
            if route.match(request):
                response = route.getResponse(request)

                if "/websocket" == request.path and "Upgrade" in request.headers and request.headers["Upgrade"] == "websocket":
                    user = isAuthenticated(request)
                    if not user:
                        return Route.buildResponse(401,{"Content-Type":"text/plain"},b'Unauthorized')
                    username = user["username"]
                    User.updateLoggedInByUsername(True, username)
                    Manager.insertClient(username,self,self.client_address)
                    self.request.sendall(response)

                    while True:
                        data = self.request.recv(1024)
                        if not data:
                            print("No data received")
                            User.updateLoggedInByUsername(False, username)
                            Manager.removeClient(username)
                            return
                        parser = WebSocketParser(bytearray(data))
                        opcode = parser.getOpcode()
                        if opcode == 8:
                            print("Opcode 8 received")
                            User.updateLoggedInByUsername(False, username)
                            Manager.removeClient(username)
                            return
                        try:
                            payload = parser.getPayload()
                        except:
                            print("Payload decoding fail")
                            User.updateLoggedInByUsername(False, username)
                            Manager.removeClient(username)
                            return
                        else:
                            handler = WebSocketHandler(payload, username)
                            Manager.sendFrame(handler)
                else:
                    return self.request.sendall(response)
        return self.request.sendall(Route.buildResponse(404,{"Content-Type":"text/plain"},b'Invalid API call'))


if __name__ == "__main__":

    print("Listening on Port 8080 . . .")
   
    print(User.selectAllUser())

    HOST, PORT = "0.0.0.0", 8000

    # Apply multithreading for webserver
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
