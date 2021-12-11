import secrets
import string
from db_init import User
from Request import Request

# Generates random character string with lowercase, uppercase alphabets and digits
def genAlphanumeric(len: int=16):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    token = [secrets.choice(chars) for _ in range(len)]
    return "".join(token)

def isAuthenticated(req: Request):
    '''
        Returns the username associated with the token.
        If no user exists (meaning user is not authenticated) return None.
    '''
    cookies = cookieParser(req)
    if 'authToken' not in cookies:
        return None
    token = cookies['authToken']
    user = User.getUserRecordByAuthToken(token) 
    if not user:
        return None
    return user

# Standard cookie parser implementation
def cookieParser(req: Request):
    cookies = {}
    if "Cookie" not in req.headers:
        return cookies
    for cookie in req.headers["Cookie"].split("; "):
        key, val = cookie.split("=",1)
        cookies[key] = val
    return cookies

