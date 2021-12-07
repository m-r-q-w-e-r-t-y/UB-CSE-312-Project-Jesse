from sockets.Socket import Socket
from db_init import User


class RetrieveUsername(Socket):

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresData(self) -> bool:
        return True

    def getReply(self, data):
        authToken = data["authToken"]
        username = User.getUsernameByAuthToken(authToken)
        if username:
            return username
        else:
            return "Unknown"
