# coding: utf8
import math
from model import ModelProducts
from config import db_options
import xlrd


def write_feat(prod_id, fr, to):
    if type(fr) is float:
        fr = int(math.ceil(fr))
    if type(to) is float:
        to = int(to)
    for i in range(fr, to+1):
        products.add_feature_value(prod_id=prod_id, feat_id=80, value=i, type='val_int')

products = ModelProducts()
products.init(db_options)
book = xlrd.open_workbook('/home/ansaev/Documents/weight.xls',formatting_info=True)
sheet = book.sheet_by_index(0)

print str(products.ok())
if products.ok():
    #get lin_in_xl(rez_data)
    print('ok')
    for row_i in range(1,sheet.nrows):
        row = sheet.row_values(row_i)
        print(int(row[0]), row[1], row[2])
        write_feat(int(row[0]), row[1], row[2])

