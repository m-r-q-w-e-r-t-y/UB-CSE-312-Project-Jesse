from sockets.Socket import Socket
from db_init import Chat


class InsertMessage(Socket):

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresBoth(self) -> bool:
        return True

    def broadcastType(self) -> str:
        return self.PAIR

    def getData(self, username, data):
        sendingTo = data["sendingTo"]
        message = data["message"]
        Chat.insertMessagesByNames(username, message, sendingTo)
        return [{"client2": sendingTo}, {username: message}]
