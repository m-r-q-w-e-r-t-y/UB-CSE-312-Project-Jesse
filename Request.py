import socketserver

class Request:
    req_type: str = None
    path: str = None
    headers: dict = {}
    body: bytes = None
    form: dict = {}

    def __init__(self, data: bytes, server: socketserver.BaseRequestHandler):
        
        # From the data in bytes, parse the headers and retrieve the request type, url and headers dictionary
        self.req_type, self.path, self.headers = Request.parseHeaders(data)

        # Check if the request is of multipart/form-data type
        if "Content-Length" in self.headers and "Content-Type" in self.headers and "multipart/form-data" in self.headers["Content-Type"]:
            bytes_needed = int(self.headers["Content-Length"])
            bytes_received = len(data) - len(data.split(b'\r\n\r\n',1)[0])

            # Accumulate buffer until we have all the bytes we need
            while bytes_received < bytes_needed:
                buffer_chunk = server.request.recv(1024)
                if not buffer_chunk:
                    break
                data += buffer_chunk
                bytes_received += len(buffer_chunk)

            # In case the headers came in chunks, re set the headers
            self.headers = Request.parseHeaders(data)[2]

            # Parse the multipart/form-data and store in dictionary
            self.form = Request.parseMultipartForm(data)

        self.body = data.split(b'\r\n\r\n',1)[1]
    
    def toString(self):
        return {
            "Http Request Type": self.req_type,
            "Path": self.path,
            "Headers": self.headers,
            "Body": self.body
        }

    @staticmethod
    def parseMultipartForm(data: bytes):
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

    @staticmethod
    def parseHeaders(data:bytes) -> dict:
        headers_dict = {}
        headers = data.split(b'\r\n\r\n',1)[0]
        headers = headers.decode("utf-8").split("\r\n")
        startline = headers[0]
        req_type,path,http_version = startline.split(" ")
        for header in headers[1:]:
            key,val = header.split(": ",1)
            headers_dict[key] = val
        return req_type, path, headers_dict
