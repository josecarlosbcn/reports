from com.files.fileWriter import FileWriter


class QueryWriter (FileWriter):
    """Constructor del lector de ficheros"""
    def __init__(self, url):
        super().__init__(url)

    def writeQuery(self, txt):
        """Escribimos en un fichero de texto"""
        with open(self.getURL(), "a") as file:
            file.write(txt + ";" + "\n")
