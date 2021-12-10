import socketserver
from WebSocketHandler import WebSocketHandler


class ClientManager:
    clients: None

    def __init__(self):
        print("Client Manager was created")
        self.clients = {}

    def insertClient(self, username: str, server: socketserver.BaseRequestHandler):
        self.clients[username] = server

    def removeClient(self, username: str):
        self.clients.pop(username)

    def sendFrame(self, handler: WebSocketHandler):
        frame = handler.getFrame()
        username = handler.getUsername()
        broadcastType = handler.getBroadcastType()

        if broadcastType == "SELF":
            self.broadcastSelf(username, frame)

        if broadcastType == "PAIR":
            data = handler.getData()
            username2 = data[0]["client2"]
            self.broadcastPair(username, username2, frame)

        if broadcastType == "ALL":
            self.broadcastAll(frame)

    def broadcastSelf(self, username: str, frame: bytes):
        client = self.clients[username]
        client.request.sendall(frame)

    def broadcastPair(self, username: str, username2: str, frame: bytes):
        client = self.clients[username]
        client.request.sendall(frame)
        try:
            client2 = self.clients[username2]
            client2.request.sendall(frame)
        except:
            print(username2 + " has logged out")

    def broadcastAll(self, frame: bytes):
        for username in self.clients:
            client = self.clients[username]
            client.request.sendall(frame)
