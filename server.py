import socketserver
import sys
from Request import Request
from WebSocketHandler import WebSocketHandler
from WebSocketParser import WebSocketParser
from routes.Route import Route
from routes.Routes import routes
from db_init import User


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

                if "/websocket" == request.path:
                    self.request.sendall(response)
                else:
                    return self.request.sendall(response)

        # Websocket
        if "Upgrade" in request.headers and request.headers["Upgrade"] == "websocket":
            print("---------------- WebSocket Zone ----------------")

            currentUser = None
            while True:
                try:
                    requestFrame = self.request.recv(1024)
                    parser = WebSocketParser(bytearray(requestFrame))
                    payload = parser.getPayload()

                    # Setting user as logged in
                    if "authToken" in payload:
                        userRecord = User.getUserRecordByAuthToken(payload["authToken"])
                        if userRecord:
                            currentUser = userRecord["username"]
                            User.updateLoggedInByUsername(True, currentUser)

                    handler = WebSocketHandler(payload)
                    self.request.sendall(handler.getFrame())
                except:

                    # Signing user off
                    if currentUser:
                        User.updateLoggedInByUsername(False, currentUser)
                    break
            print("------------------------------------------------")

        print("-------")
        # TODO: Return 404 if no routes match


if __name__ == "__main__":
    print("\n")

    print("Listening on Port 8080 . . .")
    sys.stdout.flush()
    print(User.selectAllUser())

    HOST, PORT = "0.0.0.0", 8000

    # Apply multithreading for webserver
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
