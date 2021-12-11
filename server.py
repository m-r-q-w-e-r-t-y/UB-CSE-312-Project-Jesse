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

        # If the client is requesting a file by sending a url ending with a filetype such as /signup.html, /main.css
        if Route.fileRequested(request):

            # Serve the file dynamically from the "public" folder
            response = Route.getFileDynamically(request)
            return self.request.sendall(response)

        for route in routes:

            # If the request type and path matches with a route
            if route.match(request):

                # Get the response associated with the matching route
                response = route.getResponse(request)

                # If the request is for a websocket handshake
                if "/websocket" == request.path and "Upgrade" in request.headers and request.headers["Upgrade"] == "websocket":

                    # Check if user is authenticated or not, if not send 401
                    user = isAuthenticated(request)
                    if not user:
                        return self.request.sendall(Route.buildResponse(401,{"Content-Type":"text/plain"},b'Unauthorized'))
                    username = user["username"]
                    User.updateLoggedInByUsername(True, username)
                    Manager.insertClient(username,self,self.client_address)

                    # If authenticated, send 101 response
                    self.request.sendall(response)

                    # Listen for websocket frames until client disconnects
                    while True:
                        data = self.request.recv(1024)

                        # If no data is received log out and remove user
                        if not data:
                            print("No data received")
                            User.updateLoggedInByUsername(False, username)
                            Manager.removeClient(username)
                            return

                        # Parsing frame
                        parser = WebSocketParser(bytearray(data))
                        opcode = parser.getOpcode()

                        # Opcode 8 indicates closing connection, log out and remove user
                        if opcode == 8:
                            print("Opcode 8 received")
                            User.updateLoggedInByUsername(False, username)
                            Manager.removeClient(username)
                            return

                        # Attempting to get payload
                        try:
                            payload = parser.getPayload()
                        except:
                            print("Payload decoding fail")
                            User.updateLoggedInByUsername(False, username)
                            Manager.removeClient(username)
                            return
                        else:
                            # if all checks pass, send the websocket frames to other connected users
                            handler = WebSocketHandler(payload, username)
                            Manager.sendFrame(handler)
                else:
                    # If not a websocket handshake, serve the standard HTTP response
                    return self.request.sendall(response)
        
        # If not routes match, return 404 response
        return self.request.sendall(Route.buildResponse(404,{"Content-Type":"text/plain"},b'Invalid API call'))


if __name__ == "__main__":

    print("Listening on Port 8080 . . .")
   
    print(User.selectAllUser())

    HOST, PORT = "0.0.0.0", 8000

    # Apply multithreading for webserver
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
