import codecs
import hashlib

from routes.Route import Route
from Request import Request
from routes.utility_functions import isAuthenticated


class WebSocket(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)

    def getResponse(self, request: Request) -> bytes:

        if request.req_type == "GET":
            user = isAuthenticated(request)
            if not user:
                return Route.buildResponse(401, {"Content-Type": "text/plain"},b'Unauthenticated')
            webSocketAcceptKey = self.computeAcceptKey(request.headers['Sec-WebSocket-Key'])
            return Route.buildResponse(101, {"Connection": "upgrade",
                                             "Upgrade": "websocket", "Sec-WebSocket-Accept": webSocketAcceptKey}, b'')

    @staticmethod
    def computeAcceptKey(webSocketKey):
        GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        webSocketKey += GUID
        sha1Key = hashlib.sha1(webSocketKey.encode())
        strHexKey = sha1Key.hexdigest()
        hexKey = codecs.decode(strHexKey, 'hex')
        base64Encode = codecs.encode(hexKey, 'base64')
        return base64Encode.decode("utf-8").strip()
