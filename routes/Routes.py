from typing import List
from routes.Route import Route
from routes.Signup import Signup as SignupRoute
from routes.WebSocket import WebSocket as WebSocketRoute

routes: List[Route] = [SignupRoute("/signup", ["POST"]), WebSocketRoute("/websocket", ["GET"])]
