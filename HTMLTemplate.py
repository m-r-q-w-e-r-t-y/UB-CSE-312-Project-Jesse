class HTMLTemplate:
    def __init__(self,filename: str) -> None:
        with open("./public/" + filename, "r") as html_file:
            self.html_file: str = html_file.read()

    def insertKeyVal(self,key_vals: dict) -> 'HTMLTemplate':
        for key in key_vals:
            self.html_file = self.html_file.replace(f'{{{{{key}}}}}',key_vals[key])
        return self

    def getFileBuffer(self) -> bytes:
        return self.escapeHTMLTags().encode()

    def escapeHTMLTags(self) -> str:
        self.html_file = self.html_file.replace("<","&lt;").replace(">","&gt;")
        return self.html_file