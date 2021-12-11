
class Socket:
    webSocketAction = None
    SELF = "SELF"
    ALL = "ALL"
    PAIR = "PAIR"

    def __init__(self, webSocketAction) -> None:
        self.webSocketAction: str = webSocketAction

    def match(self, action: str) -> bool:
        return self.webSocketAction == action

    @staticmethod
    def requiresData() -> bool:
        # Override in child class
        return False

    @staticmethod
    def requiresUsername() -> bool:
        # Define in child class
        return False

    @staticmethod
    def requiresBoth() -> bool:
        # Define in child class
        return False

    @staticmethod
    def broadcastType() -> str:
        # Define in child class

        # returns "SELF" to indicate frame should be sent to self
        # returns "PAIR" to indicate frame should be sent to self
        # returns "ALL" to indicate frame should be sent to self
        pass

    @staticmethod
    def getResponse():
        # Define in child class
        pass

    @staticmethod
    def getReply(data):
        # Define in child class
        pass

    @staticmethod
    def getData(username, data):
        # Define in child class
        pass
