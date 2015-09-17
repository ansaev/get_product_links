import xlwt
def write_in_xl(data):
    book = xlwt.Workbook(encoding="utf8")
    list = book.add_sheet('sheet_1')
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            list.write(r, 2 + c, label=col)
    book.save('/home/ansaev/repos/get_product_links/hey_you_13.xls')
