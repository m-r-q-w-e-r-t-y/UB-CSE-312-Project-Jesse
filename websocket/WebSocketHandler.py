from websocket.WebSocketPacker import WebSocketPacker
from sockets.Sockets import sockets

"""
Helps determine the webSocketAction, and based of frames are packed
"""
class WebSocketHandler:
    websocketActionKey = "webSocketAction"

    dataReceived = None
    action = None
    frame = None
    broadcastType = None
    username = None
    data = None

    def __init__(self, username):
        self.username = username

    # Given payload, packs the frame
    def handleResponse(self, dataReceived):

        self.dataReceived = dataReceived
        self.action = dataReceived[self.websocketActionKey]

        # For all Socket instances in sockets
        for socket in sockets:

            # Checks action of the Socket instances to self.action
            if socket.match(self.action):

                # This socket instance does require payload to get data, then packs frame
                if socket.requiresData():
                    self.data = socket.getReply(self.dataReceived)
                    self.frame = WebSocketPacker.packFrame(self.data)
                    self.broadcastType = socket.broadcastType()
                    return

                # This socket instance does require username to get data, then packs frame
                if socket.requiresUsername():
                    self.data = socket.getReply(self.username)
                    self.frame = WebSocketPacker.packFrame(self.data)
                    self.broadcastType = socket.broadcastType()
                    return

                # This socket instance does requires both payload and username to get data, then packs frame
                if socket.requiresBoth():
                    self.data = socket.getData(self.username, dataReceived)
                    self.frame = WebSocketPacker.packFrame(self.data)
                    self.broadcastType = socket.broadcastType()
                    return

                # This socket instance does not require username nor payload to get data, then packs frame
                self.frame = WebSocketPacker.packFrame(socket.getResponse())
                self.broadcastType = socket.broadcastType()
                return

    # Returns frame packed
    def getFrame(self):
        return self.frame

    # Returns data retrieved from socket instance
    def getData(self):
        return self.data

    # Returns username given in the constructor
    def getUsername(self):
        return self.username

    # Returns BroadcastType retrieved from socket instance
    def getBroadcastType(self):
        return self.broadcastType
