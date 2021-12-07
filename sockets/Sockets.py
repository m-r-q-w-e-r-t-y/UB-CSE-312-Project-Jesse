from typing import List
from sockets.Socket import Socket
from sockets.OnlineUsers import OnlineUsers as OnlineSocket
from sockets.RetrieveUsername import RetrieveUsername as UsernameSocket


sockets: List[Socket] = [OnlineSocket('ONLINE_USERS'), UsernameSocket("GET_USERNAME")]
