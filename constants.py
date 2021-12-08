status_lines = {
    101: "HTTP/1.1 101 Switching Protocols",
    200: "HTTP/1.1 200 OK",
    301: "HTTP/1.1 301 Moved Permanently",
    307: "HTTP/1.1 307 Temporary Redirect",
    400: "HTTP/1.1 400 Bad Request",
    401: "HTTP/1.1 401 Unauthorized",
    403: "HTTP/1.1 403 Forbidden",
    404: "HTTP/1.1 404 Not Found",
    500: "HTTP/1.1 500 Internal Server Error"
}

MIME_Types = {
    "txt": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "text/javascript",
    "png": "image/png",
    "jpg": "image/jpeg",
}

auth_token_salt = b'$2b$12$4KqT/W9h.OA08NfTfhg28eSHHNvVkx93X9s1Vc/w1rPzTu0ab6qZa'