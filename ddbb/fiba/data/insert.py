from com.files.queryreader import QueryReader
from com.ddbb.daomysql import DAOMySQL
from constants import DDBB
from com.files.fileWriter import FileWriter
from constants import URL
import pymysql

"""Class to insert data to any table passing its arguments"""


class InsertDataFIBA(DAOMySQL):

    def __init__(self):
        """Constructor: Exec the query passed by query_name using args like params for the query
        Returns always the last_id get it from the last data inserted"""
        super().__init__()
        self.query = QueryReader()

    def connect_ddbb(self):
        try:
            self.connection = pymysql.connect(host = DDBB.DDBB_FIBA_HOST,
                                          user = DDBB.DDBB_FIBA_USER,
                                          password = DDBB.DDBB_FIBA_PSWD,
                                          db = DDBB.DDBB_FIBA_NAME,
                                          charset = DDBB.DDBB_FIBA_CHARSET,
                                          cursorclass=pymysql.cursors.DictCursor)
            #self.connection.autocommit(True)
            self.f = FileWriter(URL.LOG)
        except:
            print("Se ha producido un error al conectar a BBDD")

    def insert_data(self, args, query_name):
        # try:
        q = self.query.getQuery(query_name)
        self.last_id = self.insertData(q, args)

    def get_last_id(self):
        return self.last_id
