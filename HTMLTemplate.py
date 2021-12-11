class HTMLTemplate:

    """
    Read in the HTML file as a string
    """
    def __init__(self,filename: str) -> None:
        with open("./private/" + filename, "r") as html_file:
            self.html_file: str = html_file.read()

    """
    Replace {{key}} in the HTML string with the dictionary values. 
    Escape any HTML characters before replacing.
    """
    def insertKeyVal(self,key_vals: dict) -> 'HTMLTemplate':
        for key in key_vals:
            val = HTMLTemplate.escapeHTMLTags(key_vals[key])
            self.html_file = self.html_file.replace(f'{{{{{key}}}}}',val)
        return self

    """
    Returns HTML file in bytes for reponse body
    """
    def getFileBuffer(self) -> bytes:
        return self.html_file.encode()

    """
    Escape HTML tags static method
    """
    @staticmethod
    def escapeHTMLTags(val: str) -> str:
        return val.replace("<","&lt;").replace(">","&gt;")