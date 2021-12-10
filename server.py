import socketserver
from Request import Request
from WebSocketHandler import WebSocketHandler
from WebSocketParser import WebSocketParser
from routes.Route import Route
from routes.Routes import routes
from db_init import User
from clientManager_init import Manager
import traceback

# Note: Handles TCP connections (request and response)
from routes.utility_functions import isAuthenticated


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # HTTP
        request = Request(self)
        print(f'{request.req_type} {request.path}')

        if Route.fileRequested(request):
            response = Route.getFileDynamically(request)
            return self.request.sendall(response)

        for route in routes:
            if route.match(request):
                response = route.getResponse(request)

                if "/websocket" == request.path:
                    self.request.sendall(response)
                else:
                    return self.request.sendall(response)

        # Handles Websocket
        if "Upgrade" in request.headers and request.headers["Upgrade"] == "websocket":
            print("---------------- WebSocket Zone ----------------")

            # Obtaining currentUser, indicate online else reroute to signup
            userRecord = isAuthenticated(request)
            if not userRecord:
                response =  Route.buildResponse(307, {"Location": "/signup"}, b'')
                return self.request.sendall(response)

            currentUser = userRecord["username"]
            User.updateLoggedInByUsername(True, currentUser)
            Manager.insertClient(currentUser, self)

            while True:
                try:
                    requestFrame = self.request.recv(1024)
                    parser = WebSocketParser(bytearray(requestFrame))
                    payload = parser.getPayload()
                    handler = WebSocketHandler(payload, currentUser)
                    Manager.sendFrame(handler)

                    # self.request.sendall(handler.getFrame())
                except Exception as e:
                    traceback.print_exc()
                    # Signing currentUser off
                    if currentUser:
                        User.updateLoggedInByUsername(False, currentUser)
                        Manager.insertClient(currentUser, self)
                    break
            print("------------------------------------------------")
        
        return self.request.sendall(Route.buildResponse(404,{"Content-Type":"text/plain"},b'Invalid API call'))


if __name__ == "__main__":

    print("Listening on Port 8080 . . .")
   
    print(User.selectAllUser())

    HOST, PORT = "0.0.0.0", 8000

    # Apply multithreading for webserver
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
