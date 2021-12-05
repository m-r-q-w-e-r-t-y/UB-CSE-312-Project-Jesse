from statusMessage import statusMessage
from paths import paths
from redirect import redirect
from extensions import extensions
from Request import Request
from HTMLFile import HTMLFile
import pymongo
import json
import hashlib, codecs
import bcrypt
import string
import secrets

# client = pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient("mongo")
db = client["database"]
info = db["clients"]

class Response:
    startLine = ""
    headers = ""
    body = ""
    mongo = info

    request = None

    # hostPath = "./sample_page/"
    # hostPath = "./HW3-WebSocketsDatabasesAPIs/sample_page/" python2
    # hostPath = "./sample_page/" # python3
    hostPath = "./webpages/"

    # request: Object
    def __init__(self, request, mongo):
        self.request = request
        self.handleResponse()
        self.mongo = mongo

    def getStartLine(self):
        return self.startLine

    def getMongo(self):
        return self.mongo
    
    def getHeaders(self):
        return self.headers

    def getBody(self):
        return self.body

    def getStatusCode(self):
        return self.startLine.split(" ")[1]

    def printRequest(self):
        string = self.startLine.strip("\r\n")[0] + "\n"

        h = self.headers.strip("\r\n")
        for line in h:
            i = line.index(":")
            k = line[::i]
            v = line[i+2::]
            string += "{}: {}\n".format(k, v)
        
        string += "\n"

        string += self.body

    def getResponse(self):
        startLine = self.startLine.encode()
        headers = self.headers.encode()
        body = self.body
        if type(body) is not bytes:
            body = self.body.encode()
        return startLine + headers + body

    def handleResponse(self):
        if self.request.getPath() in paths:
            self.handleStartLine()
            self.handleHeadersAndBody()
            # self.setCookies("Max-Age");
        else:
            self.handleNotFound()

    def handleStartLine(self):
        statusCode = paths[self.request.getPath()]
        self.startLine = "HTTP/1.1 {} {}\r\n".format(statusCode, statusMessage[statusCode])

    def handleHeadersAndBody(self):
        statusCode = self.getStatusCode()
        if statusCode == "200":
            self.handleOK()
        elif statusCode == "301":
            self.handleRedirect()
        elif statusCode == "101":
            self.handleWebSocket()
        else:
            self.handleNotFound()   

    def handleOK(self):
        # is path a file
        if "." in self.request.getPath():
            relativePath = self.request.getPath()[1::]
            print(relativePath)
            fileBytes = self.fileBytes(relativePath)
            byteLength = len(fileBytes)
            textType = "utf-8"
            fileType = extensions[relativePath[relativePath.index(".")::]]

            self.headers = "Content-Type: {}; charset=utf-8\r\n".format(fileType, textType)
            self.headers += "Content-Length: {}\r\n".format(byteLength)
            self.headers += "X-Content-Type-Options: nosniff\r\n"
            self.headers += "\r\n"
            
            self.body = "{}".format(fileBytes.decode("utf-8"))

        elif "/" == self.request.getPath():
            name = "htmlFiles/login.html"
            file = HTMLFile(self.hostPath+name)
            fileb = None
            if "Cookie" in self.request.getHeaders():
                cookieValues = self.getRequestCookies()
                visits = self.getVisits(cookieValues)
                fileb = file.updateCount(visits)
            else:
                # fileb = file.fileb.decode('utf-8')
                fileb = file.updateCount("This is the first time you are visiting this page")
            length = len(fileb)
            fileType = extensions[name[name.index(".")::]]

            self.startLine = "HTTP/1.1 200 OK\r\n"

            self.headers = "Content-Type: {}; charset=utf-8\r\n".format(fileType)                          
            self.headers += "Content-Length: {}\r\n".format(length)
            self.headers += "X-Content-Type-Options: nosniff\r\n"
            self.headers += "\r\n"

            self.setCookies("Max-Age")
            
            self.body = "{}".format(fileb)
        
        elif "/login" == self.request.getPath():
            user = self.returnUser()
            message = ""
            if self.isValidPassword(user["password"]):
                if self.isInDB(user):
                    message = "Welcome back {}".format(user["username"])
                else:
                    message = "Invalid login credentials"
                length = len(message)
                self.headers = "Content-Type: text/plain; charset=utf-8\r\n"
                self.headers += "Content-Length: {}\r\n".format(length)
                self.headers += "X-Content-Type-Options: nosniff\r\n"
                self.headers += "\r\n"
                
                self.body = message
            else:
                message = "Password did not meet requirements"
                length = len(message)
                self.headers = "Content-Type: text/plain; charset=utf-8\r\n"
                self.headers += "Content-Length: {}\r\n".format(length)
                self.headers += "X-Content-Type-Options: nosniff\r\n"
                self.headers += "\r\n"
                
                self.body = message


        elif "/signup" == self.request.getPath():
            user = self.returnUser()
            message = ""
            if self.isValidPassword(user["password"]):
                if self.isInDB(user):
                    message = "You are in the database, already. Use the login button {}".format(user["username"])
                else:
                    message = "Successfully signed up {}".format(user["username"])
                    password = user["password"].encode("utf-8")
                    salt = bcrypt.gensalt()
                    user["password"] = bcrypt.hashpw(password, salt)
                token = self.returnSessionToken()
                user["token"] = hashlib.sha256(token.encode('utf-8')).hexdigest()
                self.mongo.insert_one(user)
                length = len(message)
                self.headers = "Content-Type: text/plain; charset=utf-8\r\n"
                self.headers += "Content-Length: {}\r\n".format(length)
                self.headers += "X-Content-Type-Options: nosniff\r\n"
                self.headers += "\r\n"
                
                tempHeaders = self.headers
                cookieHeaders = "Set-Cookie: id= {}; Max-Age=3600; Secure; HttpOnly\r\n".format(self.returnSessionToken())
                self.headers = cookieHeaders + tempHeaders

                self.body = message
            else:
                message = "Password did not meet requirements"
                length = len(message)
                self.headers = "Content-Type: text/plain; charset=utf-8\r\n"
                self.headers += "Content-Length: {}\r\n".format(length)
                self.headers += "X-Content-Type-Options: nosniff\r\n"
                self.headers += "\r\n"
                
                self.body = message

    def handleWebSocket(self):
        extractedKey = self.request.getHeaders()["Sec-WebSocket-Key"] + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        sha1Key = hashlib.sha1(extractedKey.encode())
        strHexKey = sha1Key.hexdigest()
        hexKey = codecs.decode(strHexKey, 'hex')
        base64Encode = codecs.encode(hexKey, 'base64')

        self.headers = "Connection: Upgrade\r\n"
        self.headers += "Upgrade: websocket\r\n"
        self.headers += "Sec-WebSocket-Accept: {}\r\n".format(base64Encode.decode("utf-8"))

    def handleRedirect(self):
        self.headers = "Content-Length: 0\r\n"
        self.headers += "Location: {}\r\n".format(redirect[self.request.getPath()])
        self.headers += "X-Content-Type-Options: nosniff\r\n"  

    def handleNotFound(self):
        self.startLine = "HTTP/1.1 404 Not Found\r\n"

        msg = "The requested content does not exist"
        msgLen = len(msg)

        self.headers = "Content-Type: text/plain\r\n"
        self.headers += "Content-Length: {}\r\n".format(msgLen)
        self.headers += "X-Content-Type-Options: nosniff\r\n"
        self.headers += "\r\n"

        self.body = "{}".format(msg)    

    def setCookies(self, string):
        if "Cookie" not in list(self.request.getHeaders().keys()):
            # if self.request.getReqType() == "GET" and self.request.getPath == "/":
            if string == "Max-Age": 
                tempHeaders = self.headers
                cookieHeaders = "Set-Cookie: Max-Age=3600; Secure; HttpOnly; Path=/\r\n"
                cookieHeaders += "Set-Cookie: visits=1\r\n"
                self.headers = cookieHeaders + tempHeaders
        else:
            visits = int(self.getVisits(self.request.getHeaders()["Cookie"]))
            tempHeaders = self.headers
            cookieHeaders = "Set-Cookie: visits={}\r\n".format(visits+1)
            self.headers = cookieHeaders + tempHeaders
            
    def getRequestCookies(self):
        return self.request.getHeaders()["Cookie"]

    def getVisits(self, header):
        if "visits=" in header:
            visits = ""
            startIndex = header.index("visits=")+7
            tempHeaders = header[startIndex+1::]
            try:
                endIndex = tempHeaders.index(";")+startIndex+1
                for i in range(startIndex, endIndex):
                    visits += header[i]
            except:
                for i in range(startIndex, len(header)):
                    visits += header[i]
            return visits

    def fileBytes(self, relativePath):
        file = self.hostPath + relativePath
        try:
            f = open(file, 'rb')
            f_bytes = f.read()
            return f_bytes
        except Exception:
            return None

    def toString(self):
        return self.startLine + self.headers + self.body

    def returnUser(self):
        if self.request.getReqType() == "POST":
            dictionary = json.loads(self.request.getBody())
            return dictionary
        else:
            return None

    def isInDB(self, user):
        cursor = list(info.find({"username":user["username"]}))
        for obj in cursor:
            password = user["password"].encode("utf-8")
            if bcrypt.checkpw(password, obj["password"]):
                return True
        return False

    def isValidPassword(self, password):
        if len(password) < 8:
            return False
        if "@buffalo.edu" not in password:
            return False
        specialCharacters = ['~', '!', '@', '#', '$', '%', '^', '*', '-', '_', '=', '+', '[', '{', ']', '}', '/', ';', ':', ',', '.', '?']
        countLowercase = 0
        countUppercase = 0
        countNumber = 0
        countSpecial = 0
        for c in password:
            if c.islower():
                countLowercase += 1
            if c.isupper():
                countUppercase += 1
            if c.isdigit():
                countNumber += 1
            if c in specialCharacters:
                countSpecial += 1
        
        if countLowercase != 0 and countUppercase != 0 and countNumber != 0 and countSpecial != 0:
            return True
        else:
            return False

    def returnSessionToken(self):
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for i in range(32))
        return token





# Testing suite
# statusCode = "200"
# headers = {
#     "Content-Type": "text/plain"
# }
# body = "hello"
# r = Response1(statusCode, headers, body)
# print(r.getHeaders())