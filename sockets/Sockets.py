from typing import List
from sockets.Socket import Socket
from sockets.OnlineUsers import OnlineUsers as OnlineSocket
from sockets.Canvas import Canvas as CanvasSocket
from sockets.LoadChat import LoadChat as LoadChatSocket
from sockets.InsertMessage import InsertMessage as InsertMessageSocket

"""
List of all Socket instances handled by the server
"""
sockets: List[Socket] = [OnlineSocket('ONLINE_USERS'), CanvasSocket("SEND_CANVAS"),
                         LoadChatSocket("LOAD_CHAT"), InsertMessageSocket("SEND_MESSAGE")]
