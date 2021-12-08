from sockets.Socket import Socket
from db_init import User


class RetrieveProfilePic(Socket):

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresData(self) -> bool:
        return True

    def getReply(self, data):
        username = data["username"]
        profilePicPath = User.getProfilePicPathByUsername(username)
        if profilePicPath:
            return profilePicPath
        else:
            return "/error.jpeg"