from routes.Route import Route
from Request import Request
from db_init import User

class Signup(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)

    def getResponse(self, request: Request) -> bytes:   
        if request.req_type == "POST":
            form = request.form
            if ("username" not in form or 
                "password" not in form or 
                "confirm-password" not in form or
                "avatar" not in form):
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'All fields must be filled')
                 
            if form["password"] != form["confirm-password"]:
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'Password fields do not match')

            if form["file-type"] != "png" and form["file-type"] != "jpg" and form["file-type"] != "jpeg":
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'Submitted file must be an image')

            return Route.buildResponse(200,{"Content-Type":"text/plain"},b'Account created')
        elif request.req_type == "GET":
            try:
                f = open("./public/signup.html", "rb")
                file = f.read()

                return Route.buildResponse(200,{"Content-Type":"text/html"},file)
            except Exception:
                return Route.buildResponse(500, {"Content-Type":"text/plain"},b'Internal Sever Error')