from routes.Route import Route
from Request import Request

class Signup(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)

    def getResponse(self, request: Request) -> bytes:
        if request.req_type == "POST":
            return Route.buildResponse(200,{"Content-Type":"text/plain"},f'{request.form.keys()}'.encode())