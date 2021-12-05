import re

class HTMLFile:
    file = None
    fileb = None
    placeholders = None
    def __init__(self, filename):
        self.file = self.getFile(filename)
        self.fileb = self.getBytes(filename)
        self.parsePlaceholders()

    def getFile(self, filename):
        try:
            f = open(filename, 'r')
            read = str(f.read())
            return read
        except Exception:
            return None

    def getBytes(self, filename):
        try:
            f = open(filename, 'rb')
            f_bytes = f.read()
            return f_bytes
        except Exception:
            return None

    def printFile(self):
        print(self.file)
    
    def printPlaceholders(self):
        self.parsePlaceholders()
        print(self.placeholders)

    def parsePlaceholders(self):
        self.placeholders = re.findall('{{.*?}}', self.file)

    def updateCount(self, count):
        html = self.file
        for placeholder in self.placeholders:
            if placeholder == "{{count}}":
                html = self.file.replace(placeholder, str(count))
        return html

    

# html = HTMLFile("./sample_page/form.html")
# # html.printFile()
# # html.printPlaceholders()
# print(html.updateCount(20))
