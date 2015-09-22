# coding: utf8
from model import ModelProducts
from config import db_options
from view import write_in_xl
import string
import sys

reload(sys)
sys.setdefaultencoding('utf8')

products = ModelProducts()
products.init(db_options)

print str(products.ok())

rez_data = []
for i,row in enumerate(products.getProducts()):
    rez_data.append([])
    for j,cell in enumerate(row):
        rez_data[i].append(cell)
    id = row[0]
    link = products.getProductLink(id)
    rez_data[i].append(link)
write_in_xl(rez_data)
