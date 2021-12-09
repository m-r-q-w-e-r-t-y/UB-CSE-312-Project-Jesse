import socketserver

class Request:
    req_type: str = None
    path: str = None
    headers: dict = {}
    body: bytes = None
    form: dict = {}

    def __init__(self, server: socketserver.BaseRequestHandler):
        data = server.request.recv(1024)

        # Reset all object properties on receiving new request
        self.req_type = None
        self.path = None
        self.headers = {}
        self.body = None
        self.form = {}


        headers = data.split(b'\r\n\r\n',1)[0]
        headers = headers.decode("utf-8").split("\r\n")
        startline = headers[0]
        req_type,path,http_version = startline.split(" ")
        for header in headers[1:]:
            key,val = header.split(": ")
            self.headers[key] = val
        if "Content-Length" in self.headers and "Content-Type" in self.headers and "multipart/form-data" in self.headers["Content-Type"]:
            bytes_needed = int(self.headers["Content-Length"])
            bytes_received = len(data) - len(data.split(b'\r\n\r\n',1)[0])
            while bytes_received < bytes_needed:
                buffer_chunk = server.request.recv(min(1024,bytes_needed-bytes_received))
                if not buffer_chunk:
                    break
                data += buffer_chunk
                bytes_received += len(buffer_chunk)
            self.form = self.parseMultipartForm(data)
        self.req_type = req_type
        self.path = path
        self.body = data.split(b'\r\n\r\n',1)[1]
    
    def toString(self):
        return {
            "Http Request Type": self.req_type,
            "Path": self.path,
            "Headers": self.headers,
            "Body": self.body
        }
    def parseMultipartForm(self,data: bytes):
        boundary = data.split(b'Content-Type: multipart/form-data; boundary=')[1]
        boundary = b'--' + boundary.split(b'\r\n')[0]
        form_body = data.split(boundary)[1:-1]
        form = {"file-type":None}
        for field in form_body:
            name = field.split(b'"')[1].decode("utf-8")
            value = field.split(b'\r\n')[-2]
            if value == b'undefined':
                value = None
            if name == 'avatar' and value:
                filetype = field.split(b'"')[3].decode("utf-8").split(".")[-1]
                form["file-type"] = filetype
            form[name] = value
        return form