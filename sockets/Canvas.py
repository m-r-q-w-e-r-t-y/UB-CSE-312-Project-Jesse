from sockets.Socket import Socket
from db_init import User


class Canvas(Socket):

    def __init__(self, webSocketAction):
        super().__init__(webSocketAction)

    def requiresData(self) -> bool:
        return True

    def getReply(self, data):
        return {'x':data['x'], 'y':data['y']} # add "color": color