from typing import List
from routes.Route import Route
from routes.Signup import Signup as SignupRoute

routes: List[Route] = [SignupRoute("/signup",["POST"])]