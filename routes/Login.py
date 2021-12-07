from routes.Route import Route
from Request import Request

class Login(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)

    def getResponse(self, request: Request):
        if request.req_type == "POST":
            return Route.buildResponse()

        