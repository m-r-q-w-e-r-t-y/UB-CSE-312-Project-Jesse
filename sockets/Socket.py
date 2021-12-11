
class Socket:
    webSocketAction = None
    SELF = "SELF"
    ALL = "ALL"
    PAIR = "PAIR"

    # webSocketAction given is the action of the Socket instance
    def __init__(self, webSocketAction) -> None:
        self.webSocketAction: str = webSocketAction

    # Checks if given action is the same as webSocketAction define by constructor
    def match(self, action: str) -> bool:
        return self.webSocketAction == action

    # Returns bool based on whether this Socket instance need data
    @staticmethod
    def requiresData() -> bool:
        # Override in child class
        return False

    # Returns bool based on whether this Socket instance needs username
    @staticmethod
    def requiresUsername() -> bool:
        # Define in child class
        return False

    # Returns bool based on whether this Socket instance need data and username
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

    # If no data or username is required, this will be called
    @staticmethod
    def getResponse():
        # Define in child class
        pass

    # If data is required, this will be called
    @staticmethod
    def getReply(data):
        # Define in child class
        pass

    # If data and username is required, this will be called
    @staticmethod
    def getData(username, data):
        # Define in child class
        pass
