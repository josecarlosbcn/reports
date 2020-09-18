from com.files.queryreader import QueryReader
from com.ddbb.daomysql import DAOMySQL
from constants import DDBB
from com.files.fileWriter import FileWriter
from constants import URL
import pymysql

"""Class to search data from any table and arguments"""


class SearchData(DAOMySQL):

    def __init__(self, args, query_name):
        """Constructor: Exec the query passed by query_name using args like params for the query
        Returns always the last_id get it from the last data inserted"""
        super().__init__()
        query = QueryReader()
        q = query.getQuery(query_name)
        self.result = self.query(q, args)

    def connect_ddbb(self):
        try:
            self.connection = pymysql.connect(host = DDBB.DDBB_HOST,
                                          user = DDBB.DDBB_USER,
                                          password = DDBB.DDBB_PSWD,
                                          db = DDBB.DDBB_NAME,
                                          charset = DDBB.DDBB_CHARSET,
                                          cursorclass=pymysql.cursors.DictCursor)
            #self.connection.autocommit(True)
            self.f = FileWriter(URL.LOG)
        except:
            print("Se ha producido un error al conectar a DDBBFEB")

    def get_result(self):
        return self.result
