from com.ddbb.daomysql import DAOMySQL
from com.files.queryreader import QueryReader

"""Class to search data from any table and arguments"""


class SearchData:

    def __init__(self, args, query_name):
        bbdd = DAOMySQL()
        query = QueryReader()
        q = query.getQuery(query_name)
        self.result = bbdd.query(q, args)

    def get_result(self):
        return self.result
