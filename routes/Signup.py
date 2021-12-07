from routes.Route import Route
from Request import Request
from db_init import User
import bcrypt
from routes.utility_functions import genAlphanumeric
import os

class Signup(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)

    def getResponse(self, request: Request) -> bytes:   
        if request.req_type == "POST":
            form = request.form
            if ("username" not in form or 
                "password" not in form or 
                "confirm-password" not in form or
                "avatar" not in form):
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'All fields must be filled')

            password, confirm_password, username, file_type = form["password"], form["confirm-password"], form["username"], form["file-type"]

            username = username.decode("utf-8")

            if password != confirm_password:
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'Password fields do not match')

            if file_type != "jpg":
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'Submitted file must be a JPEG image')

            if User.getUserRecordByName(username):
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'Username already taken')
            
            new_filename = "uploads/" + genAlphanumeric() + ".jpg"

            try:
                with open(new_filename,"wb") as file:
                    file.write(form["avatar"])
            except Exception as e:
                print("Unexpected error occured while trying to save image ",e)
                return Route.buildResponse(500,{"Content-Type":"text/plain"},b'Failed to save image')
            else:
                hashed_password = bcrypt.hashpw(password,bcrypt.gensalt()).decode("utf-8")
                User.insertUser(username,hashed_password,new_filename)
                return Route.buildResponse(200,{"Content-Type":"text/plain"},new_filename.encode())
            finally:
                file.close()
                basepath = 'uploads/'
                print("List of images in /uploads folder:")
                for entry in os.listdir(basepath):
                    if os.path.isfile(os.path.join(basepath, entry)):
                        print(entry)