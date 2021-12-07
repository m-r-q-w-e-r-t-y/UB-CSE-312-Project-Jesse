from WebSocketPacker import WebSocketPacker
from sockets.Sockets import sockets


class WebSocketHandler:
    websocketActionKey = "webSocketAction"

    dataReceived = None
    action = None
    frame = None

    def __init__(self, dataReceived):
        self.dataReceived = dataReceived
        self.action = dataReceived[self.websocketActionKey]
        self.handleResponse()

    def handleResponse(self):
        for socket in sockets:
            if socket.match(self.action):
                if socket.requiresData():
                    response = socket.getReply(self.dataReceived)
                    self.frame = WebSocketPacker.packFrame(response)
                    return
                self.frame = WebSocketPacker.packFrame(socket.getResponse())
                return

    def getFrame(self):
        return self.frame
