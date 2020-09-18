from com.files.file import File
import jsbeautifier
from pathlib import Path


class JSONWriter (File):
    """Constructor del lector de ficheros"""
    def __init__(self, url):
        super().__init__(url)

    def writeFile(self, txt):
        """Escribimos en un fichero de texto"""
        file = Path(self.getURL())
        if not file.exists():
            content = jsbeautifier.beautify(txt)
            with open(self.getURL(), "w") as file:
                file.write(content)
        else:
            """File Exists!!!!. Don't do anything"""
            pass
