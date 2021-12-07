from sockets.Socket import Socket
from db_init import User


class OnlineUsers(Socket):
    userDb = User

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresData(self) -> bool:
        return False

    def getResponse(self):
        return self.userDb.getAllUsernames("Nil")
