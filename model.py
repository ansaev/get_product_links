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

    def add_product(self, id, cat_id, name, company_id=3, recomended_price=0, suplay_price=1234):
        # add product to products table
        product_code = 365365
        sql = "INSERT INTO `cscart`.`cscart_products` (`product_id`, `product_code`, `product_type`, `status`, `company_id`, `list_price`, `amount`, `weight`, `length`, `width`, `height`, `shipping_freight`, `low_avail_limit`, `timestamp`, `updated_timestamp`, `usergroup_ids`, `is_edp`, `edp_shipping`, `unlimited_download`, `tracking`, `free_shipping`, `feature_comparison`, `zero_price_action`, `is_pbp`, `is_op`, `is_oper`, `is_returnable`, `return_period`, `avail_since`, `out_of_stock_actions`, `localization`, `min_qty`, `max_qty`, `qty_step`, `list_qty_count`, `tax_ids`, `age_verification`, `age_limit`, `options_type`, `exceptions_type`, `details_layout`, `shipping_params`, `facebook_obj_type`, `yml_brand`, `yml_origin_country`, `yml_store`, `yml_pickup`, `yml_delivery`, `yml_adult`, `yml_cost`, `yml_export_yes`, `yml_bid`, `yml_cbid`, `yml_model`, `yml_sales_notes`, `yml_type_prefix`, `yml_market_category`, `yml_manufacturer_warranty`, `yml_seller_warranty`, `buy_now_url`, `ebay_template_id`, `product_hash`, `package_type`, `external_id`)"
        sql += " VALUES (" + str(id) + ", '" + str(product_code) + "', 'P', 'A', '" + str(company_id) + "', '" + str(
            recomended_price) + "', '999', '0.00', '0', '0', '0', '0.00', '0', '0', '0', '0', 'N', 'N', 'N', 'B', 'N', 'N', 'P', 'Y', 'N', 'N', 'Y', '10', '0', 'N', '', '0', '0', '0', '0', '', 'N', '0', 'P', 'F', 'default', 'a:5:{s:16:\"min_items_in_box\";i:0;s:16:\"max_items_in_box\";i:0;s:10:\"box_length\";i:0;s:9:\"box_width\";i:0;s:10:\"box_height\";i:0;}', '', '', '', 'N', 'N', 'Y', 'N', '0.00', 'Y', '0', '0', '', '', '', '', '', '', '', '0', '', 'Letter', '');"
        query = self.db_wrapper.sql(sql)
        # add product to products_categories table
        sql = "INSERT INTO `cscart`.`cscart_products_categories` (`product_id`, `category_id`, `link_type`, `position`)"
        sql += " VALUES ('" + str(id) + "', '" + str(cat_id) + "', 'M', '0');"
        query = self.db_wrapper.sql(sql)
        # add product description
        sql = "INSERT INTO `cscart`.`cscart_product_descriptions` (`product_id`, `lang_code`, `product`, `shortname`, `short_description`, `full_description`, `meta_keywords`, `meta_description`, `search_words`, `page_title`, `age_warning_message`, `promo_text`, `ebay_title`, `ebay_description`, `override`)"
        sql += " VALUES ('%d', 'ru', '%s', '', '', '', '', '', '', '', NULL, '', NULL, NULL, NULL);" % (id, name)
        query = self.db_wrapper.sql(sql)
        # add product price
        sql = "INSERT INTO `cscart`.`cscart_product_prices` (`product_id`, `price`, `percentage_discount`, `lower_limit`, `usergroup_id`, `start_price`)"
        sql += " VALUES ('%d', '0', '0', '1', '0', NULL);" % id
        query = self.db_wrapper.sql(sql)
        # add suplayer price
        rez = " INSERT INTO `cscart`.`cscart_product_supplay_price` (`product_id`, `currency_id`, `price`, `supplay_discount`, `mark_up`, `bank_fee`)"
        rez += " VALUES ('%d', '4', '%d', '0', '10', '0'); " % (id, suplay_price)
        return rez

    def add_picture(self, prod_id, name, img_id, type='M'):
        # register image
        sql = "INSERT INTO `cscart`.`cscart_images` (`image_id`, `image_path`, `image_x`, `image_y`)"
        sql += " VALUES (%d, '%s', '400', '400'); " % (img_id, name)
        self.db_wrapper.sql(sql)
        # link producto and image
        self.add_picture_link(prod_id=prod_id,img_id=img_id, type=type)
        return

    def add_picture_link(self, prod_id, img_id, type='M'):
        sql = "INSERT INTO `cscart`.`cscart_images_links` (`pair_id`, `object_id`, `object_type`, `image_id`, `detailed_id`, `type`, `position`)"
        sql += " VALUES (NULL, '%d', 'product', '%d', '%d', '%s', '0')" % (prod_id, img_id, img_id, type)
        self.db_wrapper.sql(sql)
        return

    def add_feature_value(self, prod_id, feat_id, value, type="variant"):
        sql = "INSERT INTO `cscart`.`cscart_product_features_values` (`feature_id`, `product_id`, `variant_id`, `value`, `value_int`, `lang_code`)"
        sql += "VALUES ('%d', '%d', " % (feat_id, prod_id)
        if "variant" is type:
            sql += " '%d', '', '0.00', 'ru');" % value
        elif "val_int" is type:
            sql += " '0', '', '%d', 'ru');" % value
        elif "val_str" is type:
            sql += " '0', '%s', '0.00', 'ru');" % value
        self.db_wrapper.sql(sql)

        return

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

    def getFeatureValue(self, prod_id, feat_id, options={}):
        sql = "SELECT `variant_id`,`value_int`,`value` FROM `cscart_product_features_values` WHERE `product_id` = " + str(
            prod_id) + " AND `feature_id` = " + str(feat_id)
        feature_values = self.db_wrapper.sql(sql)
        if len(feature_values) < 1:
            return ''
        feature_variant = feature_values[0][0]
        if feature_variant == 0:
            feature_value_int = feature_values[0][1]
            feature_value = feature_values[0][2]
            value = feature_value_int if feature_value_int is not None else feature_value
        else:
            sql = "SELECT `variant` FROM `cscart_product_feature_variant_descriptions` WHERE `variant_id` = " + str(
                feature_variant)
            rows = self.db_wrapper.sql(sql)
            if len(rows) > 0:
                if len(rows[0][0]) > 0:
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
        first_line = (lambda ls, ins: [ls[i - ins] if i > ins - 1 else '' for i in range(len(ls) + ins)])(first_line,
                                                                                                          len(rez_data[
                                                                                                                  0]))

        for i, row in enumerate(rez_data):
            id = row[0]
            feature = []
            for feat_id in features_id:
                feature.append(self.getFeatureValue(id, feat_id))
            rez_data[i] = (
                lambda l1, l2: [l1[i] if i < len(l1)  else l2[i - len(l1)] for i in range(len(l1) + len(l2))])(
                rez_data[i],
                feature)

        rez_data = (lambda rows, row_first: [rows[i - 1] if i > 0 else row_first for i in range(len(rows) + 1)])(
            rez_data, first_line)

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
            if not None is rez:
                rows = rez.fetch_row(maxrows=0)
                return rows
            else:
                return
        except MySQLdb.Error as e:
            print(e)
            return False
