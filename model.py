# coding: utf8
import MySQLdb


class DB:
    __connection = None

    def __init__(self, options={}):
        pass

    def connect(self, options):
        """ Connect to MySQL database """
        if not options:
             return False
        if not ('host' in options):
             return False
        if not ('database' in options):
             return False
        if not ('user' in options):
            return False
        if not ('password' in options):
            options.password = ''
        try:
            self.__connection = MySQLdb.connect(
                host=options['host'],
                user=options['user'],
                passwd=options['password'],
                db=options['database'],
                use_unicode=False,
                charset='utf8'
            )
            return True

        except MySQLdb.Error as e:
            print(e)
            return False

    def close(self, options={}):
        try:
            self.__connection.close()
            return True
        except MySQLdb.Error as e:
            print(e)
            return False
    def sql(self,request):
        try:
            self.__connection.query(request)
            rez = self.__connection.store_result()
            rows = rez.fetch_row(maxrows=0)
            return rows
        except MySQLdb.Error as e:
            print(e)
            return False
