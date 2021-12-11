import socketserver
from WebSocketHandler import WebSocketHandler


class ClientManager:
    clients: dict
    clientAddresses: dict

    def __init__(self):
        print("Client Manager was created")
        self.clients = {}
        self.clientAddresses = {}

    def insertClient(self, username: str, server: socketserver.BaseRequestHandler,client_address):
        self.clients[username] = server
        self.clientAddresses[client_address] = username

    def removeClient(self, username):
        self.clients.pop(username)
        self.clientAddresses = {key:val for key, val in self.clientAddresses.items() if val != username}

    def sendFrame(self, handler: WebSocketHandler):
        frame = handler.getFrame()
        username = handler.getUsername()
        broadcastType = handler.getBroadcastType()

        if broadcastType == "SELF":
            self.broadcastSelf(username, frame)

        if broadcastType == "PAIR":
            data = handler.getData()
            username2 = data["username2"]
            self.broadcastPair(username, username2, frame)

        if broadcastType == "ALL":
            self.broadcastAll(frame)

    def broadcastSelf(self, username: str, frame: bytes):
        client = self.clients[username]
        client.request.sendall(frame)

    def broadcastPair(self, username: str, username2: str, frame: bytes):
        client = self.clients[username]
        client2 = self.clients[username2]
        client.request.sendall(frame)
        client2.request.sendall(frame)

    def broadcastAll(self, frame: bytes):
        for username in self.clients:
            try:
                client = self.clients[username]
                client.request.sendall(frame)
            except Exception as e:
                print(f'Failed to broadcast to user: {username} {e}')