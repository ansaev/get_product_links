# coding: utf8
from model import DB
from config import db_options
import string
import sys
reload(sys)
sys.setdefaultencoding('utf8')
file_rezult = open('g.txt', 'w')
site = 'ecobig.ru/'

db = DB()
con = db.connect(db_options)
print str(con)
rows = db.sql('SELECT `product_id`,`product` FROM `cscart_product_descriptions`')
for row in rows:
    for cell in row:
        #print(str(cell))
        #print(', ')
        file_rezult.write(str(cell))
        file_rezult.write(', ')
    id = str(row[0])
    links = db.sql("SELECT `name`,`path` FROM `cscart_seo_names` WHERE  `type`='p' and `object_id`="+id+" limit 1 ")

    for link in links:
        rez_link = str(link[0]) + "/"
        pathes = str(link[1])
        pathes = string.split(pathes,'/')
    for path in reversed(pathes):
        links = db.sql("SELECT `name` FROM `cscart_seo_names` WHERE  `type`='c' and `object_id`="+path+" limit 1 ")
        for link in links:
            rez_link = str(link[0]) + '/' + rez_link
    rez_link = site + rez_link
    file_rezult.write(rez_link)
    file_rezult.write('\n')
    print(rez_link)


