import socketserver
from websocket.WebSocketHandler import WebSocketHandler

"""
Helps manage a list of call the client that are available
"""
class ClientManager:
    clients: dict
    clientAddresses: dict

    def __init__(self):
        print("Client Manager was created")
        self.clients = {}
        self.clientAddresses = {}

    # Adding client
    def insertClient(self, username: str, server: socketserver.BaseRequestHandler,client_address):
        self.clients[username] = server
        self.clientAddresses[client_address] = username

    # Removing client
    def removeClient(self, username):
        self.clients.pop(username)
        self.clientAddresses = {key:val for key, val in self.clientAddresses.items() if val != username}

    # Sending frames to client based on BroadcastType
    def sendFrame(self, handler: WebSocketHandler):
        frame = handler.getFrame()
        username = handler.getUsername()
        broadcastType = handler.getBroadcastType()

        # Send frame to currentUser's client only
        if broadcastType == "SELF":
            self.broadcastSelf(username, frame)

        # Send frame to currentUser's client and client2
        if broadcastType == "PAIR":
            data = handler.getData()
            username2 = data[0]["client2"]
            self.broadcastPair(username, username2, frame)

        # Send frame to all existing client and client2
        if broadcastType == "ALL":
            self.broadcastAll(frame)

    # Get client based on username and send frame
    def broadcastSelf(self, username: str, frame: bytes):
        try:
            client = self.clients[username]
            client.request.sendall(frame)
        except:
            print("Sending to self client failed")

    # Get clients based on usernames and send frame
    def broadcastPair(self, username: str, username2: str, frame: bytes):
        client = self.clients[username]
        client.request.sendall(frame)
        try:
            client2 = self.clients[username2]
            client2.request.sendall(frame)
        except:
            print(username2 + " has logged out")

    # For all users in clients send frame
    def broadcastAll(self, frame: bytes):
        for username in self.clients:
            try:
                client = self.clients[username]
                client.request.sendall(frame)
            except Exception as e:
                print(f'Failed to broadcast to user: {username} {e}')
