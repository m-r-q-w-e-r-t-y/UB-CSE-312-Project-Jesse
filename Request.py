from collections import OrderedDict

class Request:
    startLine = None
    headers = None
    body = None

    def __init__(self, byteRequest):
        req = byteRequest.decode("utf_8").split("\r\n\r\n")
        headers = req[0].split("\r\n")
        self.startLine = headers[0]

        self.headers = OrderedDict()
        for h in headers:
            if ':' in h:
                i = h.index(':')
                k = h[:i]
                v = h[i+2:]
                self.headers[k] = v

        if len(req) > 1:
            req = byteRequest.decode("utf_8")
            self.body = req[req.index("\r\n\r\n")+4::]
    
    def getStartLine(self):
        return self.startLine
    
    def getHeaders(self):
        return self.headers

    def getBody(self):
        return self.body

    def getPath(self):
        return self.startLine.split(" ")[1]

    def getReqType(self):
        return self.startLine.split(" ")[0]

    def toString(self):
        string = self.startLine + "\n"

        for key in self.headers:
            string += key + ": " + self.headers[key] + "\n"
        
        string += "\n"

        if self.body != None:
            string += self.body

        return string