from com.files.queryreader import QueryReader
from com.ddbb.daomysql import DAOMySQL
from constants import DDBB
from com.files.fileWriter import FileWriter
from constants import URL
import pymysql

"""Class to insert data to any table passing its arguments"""


class UpdateData(DAOMySQL):

    def __init__(self):
        """Constructor: Exec the query passed by query_name using args like params for the query
        Returns always the last_id get it from the last data inserted"""
        super().__init__()
        self.query = QueryReader()

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

    def update_data(self, args, query_name):
        # try:
        q = self.query.getQuery(query_name)
        self.updateData(q, args)
