from com.files.file import File
from constants import URL
import os


class QueryReader(File):
    def __init__(self):
        self.setURL(URL.FILE_QUERYS)

    def getQuery(self, queryName):
        """Abrimos el archivo de querys, la buscamos y en caso de encontrarla no comentada
        la devolvemos"""
        if len(self.getURL()) > 0:
            with open(self.getURL()) as file:
                lines = file.readlines()
                query = ""
                for l in lines:
                    if (l.startswith("#") == False):
                        if(l.startswith(queryName)  == True):
                            start = len(queryName)
                            query = l[start:]
                return query
        else:
            return None
