from com.files.file import File


class FileReader (File):
    """Constructor del lector de ficheros"""
    def __init__(self, url):
        super().__init__(url)

    def readFile(self):
        """Abrimos el archivo y devolvemos una lista con las filas del fichero
        después de haber eliminado las filas comentadas"""
        if len(self.getURL()) > 0:
            with open(self.getURL()) as file:
                lines = file.readlines()
                lista = []
                for l in lines:
                    if l.startswith("#") is False and len(l) > 0:
                        lista.append(l)
                return lista
        else:
            return None
