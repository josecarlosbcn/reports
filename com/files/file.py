

class File(object):
    def __init__(self, url):
        self.setURL(url)

    def setURL (self, url):
        self.url = url

    def getURL(self):
        return self.url
