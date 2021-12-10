from WebSocketPacker import WebSocketPacker
from sockets.Sockets import sockets


class WebSocketHandler:
    websocketActionKey = "webSocketAction"

    dataReceived = None
    action = None
    frame = None
    broadcastType = None
    username = None
    data = None

    def __init__(self, dataReceived, username):
        self.dataReceived = dataReceived
        self.action = dataReceived[self.websocketActionKey]
        self.handleResponse()
        self.username = username

    def handleResponse(self):
        for socket in sockets:
            if socket.match(self.action):

                if socket.requiresData():
                    self.data = socket.getReply(self.dataReceived)
                    self.frame = WebSocketPacker.packFrame(self.data)
                    self.broadcastType = socket.broadcastType()
                    return

                if socket.requiresUsername():
                    self.data = socket.getReply(self.username)
                    self.frame = WebSocketPacker.packFrame(self.data)
                    self.broadcastType = socket.broadcastType()
                    return

                self.frame = WebSocketPacker.packFrame(socket.getResponse())
                self.broadcastType = socket.broadcastType()
                return

    def getFrame(self):
        return self.frame

    def getData(self):
        return self.data

    def getUsername(self):
        return self.username

    def getBroadcastType(self):
        return self.broadcastType
