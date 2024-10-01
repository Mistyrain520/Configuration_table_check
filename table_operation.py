import xlrd
import config
import re
from datetime import datetime, date
import ast


class Table(object):
    def open_workbook(self, DOC_DIR, workbook):
        full_path = DOC_DIR + workbook
        # return xlrd.open_workbook(full_path, formatting_info=True)
        return xlrd.open_workbook(full_path)

    def get_head(self, doc_path, workbook, sheet_name):
        wbk = self.open_workbook(doc_path, workbook)
        sheet = wbk.sheet_by_name(sheet_name)
        head = sheet.row_values(config.HEAD)
        return head

    def get_content_by_col_name(self, doc_path, workbook, sheet_name, col_name):
        wbk = self.open_workbook(doc_path, workbook)
        sheet = wbk.sheet_by_name(sheet_name)
        head = sheet.row_values(config.HEAD)
        col_index = head.index(col_name)
        return self.get_content_by_col(doc_path, workbook, sheet_name, col_index)

    def get_content_by_col(self, doc_path, workbook, sheet_name, col_index):
        list1 = []
        wbk = self.open_workbook(doc_path, workbook)
        sheet = wbk.sheet_by_name(sheet_name)
        for i in range(config.ROW_START, sheet.nrows):
            if sheet.cell_value(i, col_index) is not "":
                list1.append(self._deal_sheet_value(wbk, sheet, i, col_index))
        return list1

    def get_content_col_by_col2name(self, doc_path, workbook, sheet_name, col_name, col_name2, value2):
        list1 = []
        wbk = self.open_workbook(doc_path, workbook)
        sheet = wbk.sheet_by_name(sheet_name)
        head = sheet.row_values(config.HEAD)
        col_index = head.index(col_name)
        col_index2 = head.index(col_name2)
        for i in range(config.ROW_START, sheet.nrows):
            if self._deal_sheet_value(wbk, sheet, i, col_index2) == value2:
                list1.append(self._deal_sheet_value(wbk, sheet, i, col_index))
        return list1

    def _deal_sheet_value(self, wbk, sheet, i, col_index):
        value = sheet.cell_value(i, col_index)
        pattern = re.compile('\d*')
        if value is None:
            return
        if value == "":
            return
        if isinstance(value, float):
            return int(value)
        if re.fullmatch(pattern, value):
            return int(value)
        if int(sheet.cell(i, col_index).ctype) == 2:
            return int(value)
        elif int(sheet.cell(i, col_index).ctype) == 3:
            data_value = xlrd.xldate_as_tuple(value, wbk.datemode)
            cell_value = datetime(*data_value[:6]).strftime("%Y-%m-%d %H:%M:%S")
            return str(cell_value)
        else:
            try:
                if type(ast.literal_eval(value)) == list:
                    return ast.literal_eval(value)
                if type(ast.literal_eval(value)) == dict:
                    return ast.literal_eval(value)
            except:
                pass
        return str(value)

    # 这几个函数不要在循环里面调用，会很慢的
    # 当col1下的值等于col_valeu1：取出col2的值
    def get_content_by_col_value(self, doc_path, workbook, sheet_name, col1: str, col_value1, col_index2: int):
        list1 = []
        wbk = self.open_workbook(doc_path, workbook)
        sheet = wbk.sheet_by_name(sheet_name)
        head = sheet.row_values(config.HEAD)
        col_index1 = head.index(col1)
        for i in range(config.ROW_START, sheet.nrows):
            if sheet.cell(i, col_index1).ctype == 6:
                continue
            if sheet.cell_value(i, col_index1) is None:
                continue
            if self._deal_sheet_value(wbk, sheet, i, col_index1) == col_value1:
                list1.append(self._deal_sheet_value(wbk, sheet, i, col_index2))
        return list1

    # 根据value1的值获取value2的值.one为True，只返回第一个查到的结果。否则返回查找的所有结果列表
    def get_cell_value(self, doc_path, workbook, sheet_name, col1, col_value1, col2, one=True):
        wbk = self.open_workbook(doc_path, workbook)
        sheet = wbk.sheet_by_name(sheet_name)
        head = sheet.row_values(config.HEAD)
        col_index1 = head.index(col1)
        col_index2 = head.index(col2)
        result = []
        for i in range(config.ROW_START, sheet.nrows):
            if sheet.cell_value(i, col_index1) is None:
                continue
            if sheet.cell(i, col_index1).ctype == 6:
                continue
            if self._deal_sheet_value(wbk, sheet, i, col_index1) == col_value1:
                if one:
                    return self._deal_sheet_value(wbk, sheet, i, col_index2)
                result.append(self._deal_sheet_value(wbk, sheet, i, col_index2))
        if one:
            return
        return result

    # 根据value1和value2的值获取value3的值
    def get_cell_value2(self, doc_path, workbook, sheet_name, col1, col_value1, col2, col_value2, col3):
        wbk = self.open_workbook(doc_path, workbook)
        sheet = wbk.sheet_by_name(sheet_name)
        head = sheet.row_values(config.HEAD)
        col_index1 = head.index(col1)
        col_index2 = head.index(col2)
        col_index3 = head.index(col3)
        for i in range(config.ROW_START, sheet.nrows):
            if sheet.cell_value(i, col_index1) is None:
                continue
            if sheet.cell(i, col_index1).ctype == 6:
                continue
            if sheet.cell_value(i, col_index2) is None:
                continue
            if sheet.cell(i, col_index2).ctype == 6:
                continue
            if self._deal_sheet_value(wbk, sheet, i, col_index1) == col_value1 and self._deal_sheet_value(wbk, sheet, i, col_index2) == col_value2:
                return self._deal_sheet_value(wbk, sheet, i, col_index3)

    # 合并一下两列变成dict，第一列要求是不重复值最好,重复则会覆盖key。{col1:col2}
    def change_two_col_dict(self, doc_path, workbook, sheet_name, col1_name: str, col2_name: str):
        wbk = self.open_workbook(doc_path, workbook)
        try:
            sheet_index = wbk.sheet_names().index(sheet_name)
            sheet = wbk.sheet_by_index(sheet_index)
            head_list = sheet.row_values(config.HEAD)
            col1 = head_list.index(col1_name)
            col2 = head_list.index(col2_name)
        except ValueError:
            print("没有找到该sheet或者colname，请检查表格sheet的名字或者中文表头", sheet_name, col1_name, col2_name)
            return
        dict1 = dict()
        for i in range(config.ROW_START, sheet.nrows):
            if not self.pass_empty(i, sheet, col1):
                continue
            else:
                if sheet.cell(i, col2).ctype == 2 and sheet.cell(i, col1).ctype == 2:  # number和number的处理
                    dict1[int(sheet.cell_value(i, col1))] = int(sheet.cell_value(i, col2))
                elif sheet.cell(i, col1).ctype == 2 and sheet.cell(i, col2).ctype == 1:  # number和string的处理
                    dict1[int(sheet.cell_value(i, col1))] = self.judge_dict(str(sheet.cell_value(i, col2)))
                elif sheet.cell(i, col1).ctype == 1 and sheet.cell(i, col2).ctype == 2:  # string和number的处理
                    dict1[str(sheet.cell_value(i, col1))] = int(sheet.cell_value(i, col2))
                else:
                    dict1[self.judge_dict(str(sheet.cell_value(i, col1)))] = self.judge_dict(str(sheet.cell_value(i, col2)))  # 非以上情况全部用str
        return dict1

    @staticmethod
    def changedict(value: str) -> dict:
        result = {}
        cell = re.split(r'[;:]', value)
        for i in range(0, len(cell)-1, 2):
            if i+1 >= len(cell):
                break
            result[cell[i]] = cell[i+1]
        return result

    @staticmethod
    def pass_empty(i, sheet, col_index):
        if not sheet.cell_value(i, col_index):
            return
        if sheet.cell(i, col_index).ctype == 6:
            return
        if str(sheet.cell_value(i, col_index)) == '0':
            return
        return True

    @staticmethod
    def judge_dict(data):
        pattern = r"^(\d*:\d*;)*(\d*:\d*)$"
        pat = re.compile(pattern)
        if re.match(pat, data):
            return Table.changedict(data)
        return data

    @staticmethod
    def cut_str(data):
        pattern = r"^(\d*,)*(\d*)*$"
        pat = re.compile(pattern)
        if re.match(pat, data):
            return re.split(r',', data)
        return data

#
#
# tb = Table()
# test = tb.change_two_col_dict(config.DOC_DIR, "/F副本表.xls", "Sheet1", "id", "first_res")
# print(test)