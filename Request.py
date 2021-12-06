class Request:
    req_type: str = None
    path: str = None
    headers: dict = {}
    body: bytes = None

    def __init__(self, data: bytes):
        headers,body = data.split(b'\r\n\r\n',1)
        headers = headers.decode("utf-8").split("\r\n")
        startline = headers[0]
        req_type,path,http_version = startline.split(" ")
        for header in headers[1:]:
            key,val = header.split(": ")
            self.headers[key] = val
        self.req_type = req_type
        self.path = path
        self.body = body
    
    def getHeaders(self):
        return self.headers.keys()

    def toString(self):
        return {
            "Http Request Type": self.req_type,
            "Path": self.path,
            "Headers": self.headers,
            "Body": self.body
        }