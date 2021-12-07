class Socket:
    webSocketAction = None

    def __init__(self, webSocketAction) -> None:
        self.webSocketAction: str = webSocketAction

    def match(self, action: str) -> bool:
        return self.webSocketAction == action

    @staticmethod
    def requiresData() -> bool:
        # Define in child class
        pass

    @staticmethod
    def getResponse():
        # Define in child class
        pass

    @staticmethod
    def getResponse(data):
        # Define in child class
        pass
