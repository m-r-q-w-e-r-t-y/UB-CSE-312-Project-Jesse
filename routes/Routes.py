from typing import List
from routes.Route import Route
from routes.Signup import Signup as SignupRoute
from routes.Login import Login as LoginRoute
from routes.WebSocket import WebSocket as WebSocketRoute
from routes.AuthTest import AuthTest as AuthTestRoute
from routes.Lobby import Lobby as LobbyRoute
from routes.Logout import Logout as LogoutRoute


routes: List[Route] = [
    LobbyRoute("/",["GET"]),
    SignupRoute("/signup",["POST", "GET"]), 
    LoginRoute("/login",["POST","GET"]),
    WebSocketRoute("/websocket", ["GET"]),
    AuthTestRoute("/test/auth",["GET"]),
    LogoutRoute("/logout",["GET"])
    ]
