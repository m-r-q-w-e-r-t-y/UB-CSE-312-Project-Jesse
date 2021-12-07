from routes.Route import Route
from Request import Request
from db_init import User
import bcrypt
from routes.utility_functions import genAlphanumeric

class Login(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)

    def getResponse(self, request: Request):
        if request.req_type == "POST":
            form = request.form

            if "username" not in form or "password" not in form:
                return Route.buildResponse(400, {"Content-Type": "text/plain"},b'Fields cannot be empty')

            username, password = form["username"].decode("utf-8"), form["password"]
            user_record = User.getUserRecordByName(username)

            if not user_record or not bcrypt.checkpw(password,user_record["password"].encode()):
                return Route.buildResponse(401, {"Content-Type": "text/plain"},b'Username or password incorrect')

            auth_token = genAlphanumeric()
            hashed_auth_token = bcrypt.hashpw(auth_token.encode(),bcrypt.gensalt())
            User.updateAuthTokenByUsername(hashed_auth_token.decode("utf-8"),username)
            return Route.buildResponse(200,{"Content-Type":"text/plain", "Set-Cookie": f'authToken={auth_token};Max-Age=3600;HttpOnly'},b'Logged in with authToken '+auth_token.encode())

        elif request.req_type == "GET":
            try:
                f = open("./public/login.html", "rb")
                file = f.read()

                return Route.buildResponse(200, {"Content-Type": "text/html"}, file)
            except Exception:
                return Route.buildResponse(500, {"Content-Type": "text/plain"}, b'Internal Sever Error')