from sockets.Socket import Socket


class Canvas(Socket):

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresData(self) -> bool:
        return True

    def broadcastType(self) -> str:
        return self.ALL

    def getReply(self, data):
        data.pop("webSocketAction")
        return data
