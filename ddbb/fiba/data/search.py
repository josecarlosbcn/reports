from com.files.queryreader import QueryReader
from com.ddbb.daomysql import DAOMySQL
from constants import DDBB
from com.files.fileWriter import FileWriter
from constants import URL
import pymysql

"""Class to search data from any table and arguments"""


class SearchDataFIBA(DAOMySQL):

    def __init__(self, args, query_name):
        """Constructor: Exec the query passed by query_name using args like params for the query
        Returns always the last_id get it from the last data inserted"""
        super().__init__()
        query = QueryReader()
        q = query.getQuery(query_name)
        self.result = self.query(q, args)

    def connect_ddbb(self):
        try:
            self.connection = pymysql.connect(host = DDBB.DDBB_FIBA_HOST,
                                          user = DDBB.DDBB_FIBA_USER,
                                          password = DDBB.DDBB_FIBA_PSWD,
                                          db = DDBB.DDBB_FIBA_NAME,
                                          charset = DDBB.DDBB_FIBA_CHARSET,
                                          cursorclass=pymysql.cursors.DictCursor)
            # print("Open the connection!!!")
            #self.connection.autocommit(True)
            self.f = FileWriter(URL.LOG)
        except:
            print("Se ha producido un error al conectar a BBDD")

    def get_result(self):
        return self.result
