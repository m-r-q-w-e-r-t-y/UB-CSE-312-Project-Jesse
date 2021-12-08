from routes.Route import Route
from Request import Request
from routes.utility_functions import isAuthenticated

class AuthTest(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)
    def getResponse(self, request: Request):
        if request.req_type == "GET":
            username = isAuthenticated(request)
            if not username:
                return Route.buildResponse(401,{"Content-Type":"text/plain"},b'Unauthorized')
            return Route.buildResponse(200,{"Content-Type":"text/plain"},b'Successfully authenticated')