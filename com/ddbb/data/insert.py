from com.files.queryreader import QueryReader
from com.ddbb.daomysql import DAOMySQL
from com.exception import DDBBException

"""Class to insert data to any table passing its arguments"""


class InsertData:

    def __init__(self):
        """Constructor: Exec the query passed by query_name using args like params for the query
        Returns always the last_id get it from the last data inserted"""
        self.bbdd = DAOMySQL()
        self.query = QueryReader()

    def insert_data(self, args, query_name):
        # try:
        q = self.query.getQuery(query_name)
        self.last_id = self.bbdd.insertData(q, args)

    def get_last_id(self):
        return self.last_id
