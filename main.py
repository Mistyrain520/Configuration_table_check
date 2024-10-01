from table_operation import Table
import config
import file
import rule
import json


def check_excel(excel_name):
    r_wbk = table.open_workbook(config.RULE_DIR, excel_name)
    d_wbk = table.open_workbook(config.DOC_DIR, excel_name[:-1])
    r_sheet = r_wbk.sheet_names()
    check_sheet(r_wbk, r_sheet, d_wbk, excel_name)


def check_sheet(r_wbk, r_sheet, d_wbk, excel_name):
    """
        :param r_wbk: 策划配置规则表

        :param r_sheet:

        :param d_wbk: 工作表，检查目标，你的策划表配置

        :param excel_name: 表名
    """
    for sheet_name in r_sheet:
        sheet = r_wbk.sheet_by_name(sheet_name)
        if sheet.nrows < 1:
            continue
        d_sheet = d_wbk.sheet_by_name(sheet_name)
        check_value(sheet, sheet_name, d_sheet, excel_name)


def check_value(sheet, sheet_name, d_sheet, excel_name):
    head_list = sheet.row_values(config.HEAD)
    d_head_list = d_sheet.row_values(config.HEAD)
    for head_name in head_list:
        if head_name == '':
            continue
        if head_name not in d_head_list:
            print(head_name, excel_name, "规则表的表头不存在配置表的表头")
            continue
        d_col = d_head_list.index(head_name)
        col = head_list.index(head_name)
        for i in range(config.ROW_START, sheet.nrows):
            if sheet.cell_value(i, col) is "":
                continue
            cell = str(sheet.cell_value(i, col)).replace('\r', '').replace('\n', '').replace('\\', '\\\\')
            try:
                # value_dict = json.loads(cell)
                value_dict = json.loads(cell, strict=False)
            except ValueError:
                print("@@@@@@@@@@@@@@@@@@@规则配置错误{}".format(cell), excel_name)
            (key, value), = value_dict.items()
            # value可以是单独字符串，列表，字典，传过去变成元组({'All': ['/sys_artist.xls', 'Sheet1', 2]},),([],)("aaa",)这样子
            # 传参：所检查的表的相关信息
            getattr(rule, config.switch[key])(value, excel_name=excel_name[:-1], sheet_name=sheet_name, col_index=d_col)


if __name__ == '__main__':
    table = Table()
    excel = file.File.get_file_dir(config.RULE_DIR, file_type=".xlsx")
    d_excel = file.File.get_file_dir(config.DOC_DIR, file_type=".xls")
    dd_excel = [i+"x" for i in d_excel]
    print(excel)
    print("策划配置表有但是规则表没有的表格（注意补充）：", list(set(dd_excel).difference(set(excel))))
    print("规则表有但是策划配置表没有的表格（可以删除）：", list(set(excel).difference(set(dd_excel))))
    for every_excel in excel:
        # if every_excel != "\D道具表.xlsx":
        #     continue
        check_excel(every_excel)



