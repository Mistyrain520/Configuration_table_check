import file
import config
import xlrd
from rule import Common
import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", action='store', required=False, help="search the string you use here")
parser.add_argument("-c", "--complete", action='store', required=False, help="search the string you use here")
args = parser.parse_args()
choose_dir = config.DOC_DIR
# choose_dir = config.RULE_DIR
START = 0
excel = file.File.get_file_dir(choose_dir, file_type=".xls")
if args.search:
    search = args.search
else:
    search = "Match"
if args.complete:
    complete = args.complete
else:
    complete = "False"
print("你查找的关键词是：", search, "@@@@@@@@@@@@@@@@@@@@@@@@")
print("(左边是列名,右边是单元格内容)", "@@@@@@@@@@@@@@@@@@@@@@@@")
print(args.complete == "True", "铁子看这里")
for e in excel:
    # if e != '\\C抽卡卡池表.xls':
    #     continue
    # print(e, "@@")
    wbk = xlrd.open_workbook(choose_dir+e)
    sheet = wbk.sheet_by_index(0)
    # head = sheet.row_values(3)
    # ncols = len(sheet.row(1))
    consolog = []
    for j in range(0, sheet.ncols):
        for i in range(START, sheet.nrows):
            if not sheet.cell_value(i, j):
                continue
            if sheet.cell(i, j) == 6:
                continue
            if complete == "True":
                # print(Common.change_format(sheet.cell_value(i, j)), search,)
                if str(Common.change_format(sheet.cell_value(i, j))) == search:
                    consolog.append((sheet.cell_value(3, j), Common.change_format(sheet.cell_value(i, j))))
                continue
            if complete == "Regular":
                pat = re.compile(search)
                if re.search(pat, str(Common.change_format(sheet.cell_value(i, j)))):
                    consolog.append((sheet.cell_value(3, j), Common.change_format(sheet.cell_value(i, j))))
                continue
            if str(search) in str(sheet.cell_value(i, j)):
                consolog.append((sheet.cell_value(3, j), Common.change_format(sheet.cell_value(i, j))))
    if len(consolog) > 0:
        print("--------------------------------表格名字:{}----------------------------------------".format(e))
        print(consolog)

