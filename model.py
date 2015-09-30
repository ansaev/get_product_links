# coding: utf8
import MySQLdb
import string
from config import site


class Model(object):
    db_wrapper = None
    gg = 'hey you'

    def __init__(self):
        self.db_wrapper = DB_MySQL_wrapper()

    def init(self, options):

        self.db_wrapper.init(options)
        if self.db_wrapper.ok():
            return True
        else:
            return False

    def ok(self):
        if self.db_wrapper and self.db_wrapper.ok():
            return True
        return False


class ModelProducts(Model):
    def getProducts(self, options={}):
        if not 'avaible_cats' in options:
            options['avaible_cats'] = True
        sql = "SELECT `cscart_product_descriptions`.`product_id`,`cscart_product_descriptions`.`product` FROM `cscart_product_descriptions` LEFT JOIN `cscart_products_categories` ON `cscart_products_categories`.`product_id` =  `cscart_product_descriptions`.`product_id` WHERE `cscart_products_categories`.`category_id` in (SELECT `category_id` FROM `cscart_categories` WHERE " + " `status`='A' " + ") "
        products = self.db_wrapper.sql(sql)
        if products:
            return products
        else:
            return False

    def getCatLink(self, id):
        sql = "SELECT `name` FROM `cscart_seo_names` WHERE  `type`='c' and `object_id`=" + id + " limit 1 "
        row = self.db_wrapper.sql(sql)
        return row[0][0]

    def __getProductLink(self, id, options={}):
        sql = "SELECT `name`,`path` FROM `cscart_seo_names` WHERE  `type`='p' and `object_id`=" + str(id) + " limit 1 "
        link = self.db_wrapper.sql(sql)
        if not link:
            return False
        rez_link = {}
        rez_link['link'] = link[0][0]
        rez_link['path'] = string.split(link[0][1], '/') if len(string.split(link[0][1], '/')) > 0 else False
        return rez_link

    def getProductLink(self, id, options={}):
        link = self.__getProductLink(id)
        cats_link = ''
        for k, numb in enumerate(link['path']):
            cats_link += '/' + self.getCatLink(numb)
        cats_link = site + cats_link + '/' + link['link'] + '/'
        return cats_link

    def getProductsLinksData(self, options={}):
        rez_data = []
        for i, row in enumerate(self.getProducts()):
            rez_data.append([])
            for j, cell in enumerate(row):
                rez_data[i].append(cell)
            id = row[0]
            link = self.getProductLink(id)
            rez_data[i].append(link)
        return rez_data

    def getFeatureName(self, feature_id, options={}):
        if not 'lang' in options:
            options['lang'] = 'ru'
        sql = "SELECT `description` FROM `cscart_product_features_descriptions`WHERE `lang_code`= '" + options[
            'lang'] + "' AND `feature_id` = " + str(feature_id)
        rows = self.db_wrapper.sql(sql)
        if len(rows) < 1:
            return ''
        if len(rows[0]) < 1:
            return ''
        row = rows[0][0]
        return row

    def getProductFeaturesIds(self, prod_id, options={}):
        sql = "SELECT `feature_id` FROM `cscart_product_features_values` WHERE `product_id` = " + str(prod_id)
        features = self.db_wrapper.sql(sql)
        rez_fetures_ids = []
        if len(features) > 0:
            for feat_id_list in features:
                if len(feat_id_list) > 0:
                    rez_fetures_ids.append(feat_id_list[0])

        if len(rez_fetures_ids) > 0:
            return rez_fetures_ids
        else:
            return False

    def getFeatureValue(self, prod_id, feat_id, options = {}):
        sql = "SELECT `variant_id`,`value_int`,`value` FROM `cscart_product_features_values` WHERE `product_id` = " + str(prod_id) + " AND `feature_id` = " + str(feat_id)
        feature_values = self.db_wrapper.sql(sql)
        if len(feature_values) < 1:
            return ''
        feature_variant = feature_values[0][0]
        if feature_variant == 0:
            feature_value_int = feature_values[0][1]
            feature_value = feature_values[0][2]
            value = feature_value_int if feature_value_int is not None else feature_value
        else:
            sql = "SELECT `variant` FROM `cscart_product_feature_variant_descriptions` WHERE `variant_id` = " + str(feature_variant)
            rows = self.db_wrapper.sql(sql)
            if len(rows) > 0:
                if len(rows[0][0]) >0:
                    value = rows[0][0]
        return value

    def getProductsLinksDataExtended(self, options={}):
        rez_data = self.getProductsLinksData()
        features_id = []
        for i, row in enumerate(rez_data):
            id = row[0]
            prod_ids = self.getProductFeaturesIds(id)
            if not prod_ids:
                continue
            if len(features_id) > 0:
                for el_ex in prod_ids:
                    exist = False
                    for el_in in features_id:
                        if el_in == el_ex:
                            exist = True
                    if not exist:
                        features_id.append(el_ex)
            else:
                features_id = prod_ids

        first_line = []
        for feat_id in features_id:
            first_line.append(self.getFeatureName(feat_id))
        first_line = (lambda ls, ins: [ls[i-ins] if i > ins-1 else '' for i in range(len(ls) + ins)])(first_line, len(rez_data[0]))

        for i, row in enumerate(rez_data):
            id = row[0]
            feature = []
            for feat_id in features_id:
                feature.append(self.getFeatureValue(id, feat_id))
            rez_data[i] = (lambda l1, l2: [l1[i] if i < len(l1)  else l2[i - len(l1)] for i in range(len(l1) + len(l2))])(rez_data[i], feature)

        rez_data = (lambda rows, row_first:[rows[i-1] if i>0 else row_first for i in range(len(rows) + 1)])(rez_data, first_line)

        return rez_data


class DB_MySQL_wrapper(object):
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
