class HTMLTemplate:
    def __init__(self,filename: str) -> None:
        with open("./private/" + filename, "r") as html_file:
            self.html_file: str = html_file.read()

    def insertKeyVal(self,key_vals: dict) -> 'HTMLTemplate':
        for key in key_vals:
            val = HTMLTemplate.escapeHTMLTags(key_vals[key])
            self.html_file = self.html_file.replace(f'{{{{{key}}}}}',val)
        return self

    def getFileBuffer(self) -> bytes:
        return self.html_file.encode()

    @staticmethod
    def escapeHTMLTags(val: str) -> str:
        return val.replace("<","&lt;").replace(">","&gt;")