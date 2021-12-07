from routes.Route import Route
from Request import Request

class Login(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)

    def getResponse(self, request: Request):
        if request.req_type == "POST":
            return Route.buildResponse()
        elif request.req_type == "GET":
            try:
                f = open("./public/login.html", "rb")
                file = f.read()
                file_length = str(len(file))

                return Route.buildResponse(200, {"Content-Type": "text/html"}, file)
            except Exception:
                return Route.buildResponse(500, {"Content-Type": "text/plain"}, b'Internal Sever Error')