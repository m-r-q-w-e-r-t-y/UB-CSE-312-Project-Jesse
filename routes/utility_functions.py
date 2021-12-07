import secrets
import string

def genAlphanumeric(len: int=16):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    token = [secrets.choice(chars) for _ in range(len)]
    return "".join(token)
