import socketserver

class Request:
    req_type: str = None
    path: str = None
    headers: dict = {}
    body: bytes = None

    def __init__(self, server: socketserver.BaseRequestHandler):
        data = server.request.recv(1024)
        headers = data.split(b'\r\n\r\n',1)[0]
        headers = headers.decode("utf-8").split("\r\n")
        startline = headers[0]
        req_type,path,http_version = startline.split(" ")
        for header in headers[1:]:
            key,val = header.split(": ")
            self.headers[key] = val

        if "Content-Length" in self.headers and "Content-Type" in self.headers and "multipart/form-data" in self.headers["Content-Type"]:
            bytes_needed = int(self.headers["Content-Length"])
            bytes_received = len(data) - len(data.split(b'\r\n\r\n')[0])
            while bytes_received < bytes_needed:
                buffer_chunk = server.request.recv(1024)
                if not buffer_chunk:
                    break
                data += buffer_chunk
                bytes_received += len(buffer_chunk)
        
        self.req_type = req_type
        self.path = path
        self.body = data.split(b'\r\n\r\n',1)[1]
    
    def getHeaders(self):
        return self.headers.keys()

    def toString(self):
        return {
            "Http Request Type": self.req_type,
            "Path": self.path,
            "Headers": self.headers,
            "Body": self.body
        }