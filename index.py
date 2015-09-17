# coding: utf8
from model import ModelProducts
from config import db_options
from view import write_in_xl
import string
import sys

reload(sys)
sys.setdefaultencoding('utf8')

site = 'ecobig.ru/'

products = ModelProducts()
products.init(db_options)

print str(products.ok())

print(products.getProducts())
"""
rows = db.sql(
    "SELECT `cscart_product_descriptions`.`product_id`,`cscart_product_descriptions`.`product` FROM `cscart_product_descriptions` LEFT JOIN `cscart_products_categories` ON `cscart_products_categories`.`product_id` =  `cscart_product_descriptions`.`product_id` WHERE `cscart_products_categories`.`category_id` in (SELECT `category_id` FROM `cscart_categories` WHERE `status`='A') ")
rez_data = []
for row in rows:
    data_row = []
    for cell in row:
        data_row.append(str(cell))

    id = str(row[0])
    links = db.sql("SELECT `name`,`path` FROM `cscart_seo_names` WHERE  `type`='p' and `object_id`=" + id + " limit 1 ")

    for link in links:
        rez_link = str(link[0]) + "/"
        pathes = str(link[1])
        pathes = string.split(pathes, '/')
    for path in reversed(pathes):
        links = db.sql("SELECT `name` FROM `cscart_seo_names` WHERE  `type`='c' and `object_id`=" + path + " limit 1 ")
        for link in links:
            rez_link = str(link[0]) + '/' + rez_link
    data_row.append(site + rez_link)
    rez_data.append(data_row)

write_in_xl(rez_data)
"""
