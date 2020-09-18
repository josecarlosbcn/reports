from constants import RESULT


class ResultData(object):
    """Objeto que contendrá el resultado de una consulta"""
    def __init__(self, result, data, totalRows):
        self.setResult(result)
        self.setTotalRows(totalRows)
        self.setData(data)


    """Setters & Getters"""
    def setResult(self, result):
        self.result = result

    def getResult(self):
        return self.result

    def setTotalRows(self, tr):
        if tr != None:
            self.totalRows = int(tr)
        else:
            self.totalRows = None

    def getTotalRows(self):
        return self.totalRows

    def setData(self, data):
        """Diccionario que contiene los datos devueltos desde la BBDD"""
        if self.getTotalRows() != None and data != None:
            self.data = data.copy()
        else:
            self.data = None

    def getData(self):
        return self.data
