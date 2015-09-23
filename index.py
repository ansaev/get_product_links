# coding: utf8
from model import ModelProducts
from config import db_options
from view import write_in_xl

products = ModelProducts()
products.init(db_options)
print str(products.ok())
if products.ok():
    #get links to all products
    rez_data = products.getProductsLinksData()
    write_in_xl(rez_data)
