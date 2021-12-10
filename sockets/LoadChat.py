from sockets.Socket import Socket
from db_init import Chat


class LoadChat(Socket):

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresBoth(self) -> bool:
        return True

    def broadcastType(self) -> str:
        return self.SELF

    def getData(self, username, data):
        userClicked = data["userClicked"]
        messages = Chat.getConversationByNames(username, userClicked)
        return messages
