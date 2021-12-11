from sockets.Socket import Socket
from db_init import User


class OnlineUsers(Socket):

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresUsername(self) -> bool:
        return True

    def broadcastType(self) -> str:
        return self.SELF

    def getReply(self, username):
        usernames = User.getLoggedInUsers(username)
        profilePics = User.getLoggedInPics(username)

        return [usernames, profilePics]
