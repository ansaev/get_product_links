# coding: utf8
import MySQLdb


class ModelProducts:
    __db_wrapper = None

    def __init__(self):
        self.__db_wrapper = DB_MySQL_wrapper()

    def init(self, options):

        self.__db_wrapper.init(options)
        if self.__db_wrapper.ok():
            return True
        else:
            return False

    def ok(self):
        if self.__db_wrapper and self.__db_wrapper.ok():
            return True
        return False

    def getProducts(self, options={}):
        if not 'avaible_cats' in options:
            options['avaible_cats'] = True

        products = []
        sql = "SELECT `cscart_product_descriptions`.`product_id`,`cscart_product_descriptions`.`product` FROM `cscart_product_descriptions` LEFT JOIN `cscart_products_categories` ON `cscart_products_categories`.`product_id` =  `cscart_product_descriptions`.`product_id` WHERE `cscart_products_categories`.`category_id` in (SELECT `category_id` FROM `cscart_categories` WHERE " + " `status`='A' " + ") "
        products = self.__db_wrapper.sql(sql)
        if products:
            return products
        else:
            return False


class DB_MySQL_wrapper:
    __connection = None

    def __init__(self):
        pass

    def ok(self):
        if self.__connection:
            return True
        return False

    def init(self, options):
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

    def sql(self, request):
        try:
            self.__connection.query(request)
            rez = self.__connection.store_result()
            rows = rez.fetch_row(maxrows=0)
            return rows
        except MySQLdb.Error as e:
            print(e)
            return False
