from typing import List
from routes.Route import Route
from routes.Signup import Signup as SignupRoute
from routes.Login import Login as LoginRoute
from routes.WebSocket import WebSocket as WebSocketRoute


routes: List[Route] = [
    SignupRoute("/signup",["POST", "GET"]), 
    LoginRoute("/login",["POST","GET"]),
    WebSocketRoute("/websocket", ["GET"])
    ]
