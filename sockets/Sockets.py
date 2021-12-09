from typing import List
from sockets.Socket import Socket
from sockets.OnlineUsers import OnlineUsers as OnlineSocket
from sockets.Canvas import Canvas as CanvasSocket


sockets: List[Socket] = [OnlineSocket('ONLINE_USERS'), CanvasSocket("SEND_CANVAS")]
