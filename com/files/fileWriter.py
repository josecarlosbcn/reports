from com.files.file import File
from datetime import datetime


class FileWriter (File):
    """Constructor del lector de ficheros"""
    def __init__(self, url):
        super().__init__(url)

    def writeFile(self, txt):
        """Escribimos en un fichero de texto"""
        with open(self.getURL(), "a") as file:
            file.write(str(datetime.today()) + ": " + txt + "\n")
