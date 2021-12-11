from routes.Route import Route
from Request import Request
from routes.utility_functions import isAuthenticated
from HTMLTemplate import HTMLTemplate

class Lobby(Route):
    """
    Route to handle GET /lobby. Performs authentication and if user is authenticated shows lobby.html with username and profile pic 
    rendered in the HTML via custom templating
    """
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)
    def getResponse(self, request: Request):
        if request.req_type == "GET":
            user = isAuthenticated(request)
            if not user:
                return Route.buildResponse(307,{"Location":"/signup"},b'')
            username,profile_pic_path = user["username"],user["profilePicPath"]
            try:
                html_template = HTMLTemplate("lobby.html").insertKeyVal({"username":username,"profile_pic_path":profile_pic_path}).getFileBuffer()
                return Route.buildResponse(200,{"Content-Type":"text/html; charset=utf-8"},html_template)
            except Exception as e:
                print(e)
                return Route.buildResponse(500,{"Content-Type":"text/plain"},b'Internal Server Error')
                
            

