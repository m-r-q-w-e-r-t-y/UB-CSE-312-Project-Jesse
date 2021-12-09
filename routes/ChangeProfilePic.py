from routes.Route import Route
from Request import Request
from routes.utility_functions import isAuthenticated

class ChangeProfilePic(Route):
    def __init__(self, path, methods) -> None:
        super().__init__(path, methods)

    def getResponse(self, request: Request):
        if request.req_type == "POST":
            user = isAuthenticated(request)
            if not user:

                # Cannot change profile pic of unauthenticated users
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'Bad Request')
            
            form = request.form
            if "avatar" not in form or "file-type" not in form or form["file-type"] != "jpg":

                # If no image sent with request or if image is not jpg return 400 
                return Route.buildResponse(400,{"Content-Type":"text/plain"},b'Bad Request')
            
            profile_pic_path = user["profilePicPath"]
            new_file = form["avatar"]

            # Keep the same name but update the image file
            try:
                with open(profile_pic_path,"wb") as file:
                    file.write(new_file)
                
                # If file write successful, redirect user to lobby
                return Route.buildResponse(303,{"Location":"/"},b'')
            except Exception:
                return Route.buildResponse(500,{"Content-Type":"text/plain"},b'Internal Server Error')

