from constants import RESULT
from com.ddbb.resultdata import ResultData
import abc


class DAOMySQL(metaclass=abc.ABCMeta):
    def __init__(self):
        """Constructor: Conectamos con la BBDD"""
        self.connection = None
        self.connect_ddbb()

    @abc.abstractmethod
    def connect_ddbb(self):
        raise NotImplementedError("DAOMySQL", "connect_ddbb", None,
                                  "El usuario no ha implementado el método")

    def __del__(self):
        """Destructor: Cerramos la conexión con la BBDD"""
        # print("Close the connection!!!")
        self.connection.close()

    def query(self, sql, data):
        """Método que devuelve un objeto ResultData con el resultado de la consulta"""
        # try:
        with self.connection.cursor() as cursor:
            totalRows = cursor.execute(sql, data)
            #print("Total Rows: " + str(totalRows))
            #print("Ultima query: " + cursor.mogrify(sql, data))
            data = cursor.fetchall()
            if totalRows > 0:
                result = ResultData(RESULT.RESULT_OK, data, totalRows)
            else:
                result = ResultData(RESULT.RESULT_OK, None, totalRows)
            return result
        # except Exception as error:
        #     raise Exception("DAOMySQL", "query", error,
        #                         "Se ha producido un error al hacer la consulta")
        # finally:
        #     #Código que se ejecuta siempre
        #     cursor.close()

    def insertData(self, sql, data):
        # try:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, data)
            self.connection.commit()
            result = ResultData(RESULT.RESULT_OK, None, None)
            #qw =  QueryWriter(urlFileSQL)
            #qw.writeQuery(cursor.mogrify(sql, data))
            return cursor.lastrowid
        # except Exception as ex:
        #     raise DDBBException("DAOMySQL", "insertData", ex,
        #         "Se ha producido un error al hacer el insert en BBDD")
        # finally:
        #     #Código que se ejecuta siempre
        #     pass

    def removeData(self, sql, data):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, data)
            self.connection.commit()
            result = ResultData(RESULT.RESULT_OK, None, None)
            #qw =  QueryWriter(urlFileSQL)
            #qw.writeQuery(cursor.mogrify(sql, data))

    def updateData(self, sql, data):
        # try:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, data)
            self.connection.commit()
            result = ResultData(RESULT.RESULT_OK, None, None)
