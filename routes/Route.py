from typing import List
from Request import Request
from constants import MIME_Types, status_lines

class Route:
    def __init__(self,path,methods) -> None:
        self.path: str = path
        self.methods: List[str] = methods

    def match(self,request: Request) -> bool:
        return self.path == request.path and request.req_type in self.methods

    @staticmethod
    def buildResponse(http_code: int,headers: dict,body: bytes) -> bytes:

        if not body:
            body = b''
        if type(body) is not bytes:
            body = body.encode()

        response = b''

        status_line = status_lines[http_code].encode()
        response += status_line
        response += b'\r\n'

        if "Content-Length" not in headers:
            headers["Content-Length"] = len(body)
        if "X-Content-Type-Options" not in headers:
            headers["X-Content-Type-Options"] = "nosniff"

        for header in headers:
            response += f'{header}: {headers[header]}\r\n'.encode()
        response += b'\r\n'

        response += body
        return response

    @staticmethod
    def fileRequested(request: Request) -> bool:
        if request.req_type != "GET": 
            return False
        file_type = request.path.split(".",1)[-1]
        return file_type in MIME_Types
    
    @staticmethod
    def getFileDynamically(request: Request) -> bytes:
        filename = request.path.split("/")[-1]
        filetype = filename.split(".")[-1]
        try:
            file = open("./public/" + filename,"rb")
            file = file.read()
            return Route.buildResponse(200,{ "Content-Type": f'{MIME_Types[filetype]}; charset=utf-8'},file)

        except Exception:
            print(f'Error while reading file {filename}: {Exception}')
            return None

    


        




