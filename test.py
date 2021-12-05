hostpath = "/webpages/cssFiles/main.css"

def extractHtml(url):
    url = url.split("/")
    file = url.pop()
    extension = file[file.index(".")+1::]
    print(extension)

extractHtml(hostpath)