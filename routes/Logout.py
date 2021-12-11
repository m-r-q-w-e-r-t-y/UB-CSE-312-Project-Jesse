from routes.Route import Route
from Request import Request
from routes.utility_functions import isAuthenticated

class Logout(Route):
    """
    GET /logout that simply states the authToken to an empty value this loggin out the user
    """
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)
    def getResponse(self, request: Request):
        if request.req_type == "GET":
            # Set the authToken to an empty string which expires in 100 seconds
            return Route.buildResponse(307,{"Set-Cookie":"authToken=\'\';Max-Age=100;HttpOnly", "Location":"/"},b'')

