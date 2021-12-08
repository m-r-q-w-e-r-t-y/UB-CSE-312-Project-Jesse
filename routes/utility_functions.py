import secrets
import string
from db_init import User
import bcrypt
from Request import Request
from constants import auth_token_salt

def genAlphanumeric(len: int=16):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    token = [secrets.choice(chars) for _ in range(len)]
    return "".join(token)

def isAuthenticated(req: Request):
    '''
        Returns the username associated with the token.
        If no username exists (meaning user is not authenticated) return None.
    '''
    cookies = cookieParser(req)
    if 'authToken' not in cookies:
        return None
    token = cookies['authToken']
    if type(token) is not bytes:
        token = token.encode()
    hashed_token = bcrypt.hashpw(token,auth_token_salt)
    username = User.getUsernameByAuthToken(hashed_token) 
    if not username:
        return None
    return username

def cookieParser(req: Request):
    cookies = {}
    if "Cookie" not in req.headers:
        return cookies
    for cookie in req.headers["Cookie"].split("; "):
        key, val = cookie.split("=")
        cookies[key] = val
    return cookies

