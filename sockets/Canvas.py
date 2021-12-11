from sockets.Socket import Socket

"""
Handles websockets that sends a pointMap of a canvas location, this gets broadcast to all users
"""
class Canvas(Socket):

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresData(self) -> bool:
        return True

    def broadcastType(self) -> str:
        return self.ALL

    def getReply(self, data: dict):
        data.pop("webSocketAction")
        return data
