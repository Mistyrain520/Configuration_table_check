from collections import Counter
from table_operation import Table
import config
import re
import ast

# r_wbk  指数据配置表中对应规则表的那个表（也就是数据表）
# d_wbk  指数据配置表中对应规则表配置的规则所指向的那个表（也就是我配的规则里写的那个表）
# 比如我在A表中配置了规则指向了B表，r_wbk指A表，d_wbk指B表。


class Only(object):
    def __init__(self, *args, **kwargs):
        self.excel_name = kwargs["excel_name"]
        self.sheet_name = kwargs["sheet_name"]
        self.col_index = kwargs["col_index"]
        self.args = args
        self.wbk = table.open_workbook(config.DOC_DIR, self.excel_name)
        self.r_sheet = self.wbk.sheet_by_name(self.sheet_name)
        r_head = self.r_sheet.row_values(config.HEAD_CN)
        self.col_index_name = r_head[self.col_index]
        if self.args[0] == "All":
            self.check_all_only()
        if self.args[0] == "Every":
            self.check_every_only()

    #   规则：{"_Only":"All"}
    # 本列不允许存在重复值
    def check_all_only(self):
        col_list = table.get_content_by_col(
            config.DOC_DIR,
            self.excel_name,
            self.sheet_name,
            self.col_index)
        result = agent.list_only(col_list)
        if result:
            agent.pri_excel(
                name=self.excel_name,
                sheet=self.sheet_name,
                col=self.col_index_name)
            print("规则：本列不允许存在重复值")

    #   规则：{"_Only":"Every"}
    #   本列所有单元格，每个单元格里面的数据各自唯一（该单元格为列表）
    def check_every_only(self):
        for i in range(config.ROW_START, self.sheet.nrows):
            try:
                if isinstance(
                    ast.literal_eval(
                        self.r_sheet.cell_value(
                            i,
                            self.col_index)),
                        list):
                    cell_value = ast.literal_eval(
                        self.r_sheet.cell_value(i, self.col_index))
                    result = agent.list_only(list(cell_value))
                    if result:
                        print("表名-{}-sheet名-{}-第几行-{}-第几列-{}  该值配置不正确，里面有重复的值  {}". format(
                            self.excel_name, self.sheet_name, i, self.col_index_name, cell_value))
            except ValueError:
                print("表名-{}-sheet名-{}-第几行-{}-第几列-{}  该值配置可能不正确  {}". format(
                    self.excel_name, self.sheet_name, i, self.col_index_name, cell_value))


class Ainb(object):
    def __init__(self, *args, **kwargs):
        # **kwargs 记录正在检查的表格的相关信息
        # r_wbk  指数据配置表中对应规则表的那个表（也就是数据表）
        # d_wbk  指数据配置表中对应规则表配置的规则所指向的那个表（也就是我配的规则里指向的那个表）
        self.excel_name = kwargs["excel_name"]
        self.sheet_name = kwargs["sheet_name"]
        self.col_index = kwargs["col_index"]
        self.args = args
        self.r_wbk = table.open_workbook(config.DOC_DIR, self.excel_name)
        self.r_sheet = self.r_wbk.sheet_by_name(self.sheet_name)
        r_head = self.r_sheet.row_values(config.HEAD_CN)
        self.col_index_name = r_head[self.col_index]
        temp = {"All": "all_in",
                "Assign": "assign_in",
                "Part": "part_in",
                "Sequence": "sequence",
                "Whenassign": "whenassign",
                "Whenpoint": "whenpoint",
                "Every": "every_in",
                "Neighbor": "neighbor",
                "Allpoint": "allpoint"}
        if isinstance(self.args[0], dict):
            (key, value), = self.args[0].items()
            self.__getattribute__(temp[key])(value)

    # 每个单元格都in指定的表格指定列的合集
    # {"_In":{"All":["/sys_card.xls","Sheet1","cs_id"]}}
    def all_in(self, _value):
        d_wbk = table.open_workbook(config.DOC_DIR, _value[0])
        d_sheet = d_wbk.sheet_by_name(_value[1])
        d_head = d_sheet.row_values(config.HEAD)
        d_index = d_head.index(_value[2])
        d_col_list = table.get_content_by_col(
            config.DOC_DIR, _value[0], _value[1], d_index)
        d_col_list1 = [str(j) for j in d_col_list]
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            temp = Common.change_format(
                self.r_sheet.cell_value(
                    i, self.col_index))
            if str(temp) not in d_col_list1:
                agent.pri_excel(
                    self.excel_name,
                    self.sheet_name,
                    i,
                    self.col_index_name)
                print("规则：每个单元格都in指定的表格指定列的合集。数据:::{}--{}". format(
                    str(self.r_sheet.cell_value(i, self.col_index)), _value))

    # {"_In":{"Assign":[1,0]}}
    # 每个单元格都存在于由你设定的合集
    def assign_in(self, _value):
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            temp = Common.change_format(
                self.r_sheet.cell_value(
                    i, self.col_index))
            if temp not in _value:
                agent.pri_excel(
                    self.excel_name,
                    self.sheet_name,
                    i,
                    self.col_index)
                print("{}{}--{}--{}--{}--该数据没有存在于{}". format(self.excel_name,
                                                             self.sheet_name, i, self.col_index_name, temp, _value))

    # {"_In":{"Neighbor":[100,"des"]}}
    # 本列除以100，算出来的值，存在于另外一列（字符串）中
    def neighbor(self, _value):
        times = int(_value[0])
        col_value = _value[1]
        r_head = self.r_sheet.row_values(config.HEAD)
        target_col = r_head.index(col_value)
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            temp = Common.change_format(
                self.r_sheet.cell_value(
                    i, self.col_index))
            target = Common.change_format(
                self.r_sheet.cell_value(i, target_col))
            if str(int(temp / times)) not in target:
                agent.pri_excel(
                    self.excel_name,
                    self.sheet_name,
                    i,
                    self.col_index_name)
                print("请检查数值{}----{}".format(temp, target))

    # {"_In":{"Part":{"star":"[0,(1,11)]"}}}
    # 同个表，取出star为0值时，本列的所有值，判断值满足(1,10)范围
    def part_in(self, _value):
        (key, value), = _value.items()
        col = key
        col_value = ast.literal_eval(value)[0]
        min_value = ast.literal_eval(value)[1][0]
        max_value = ast.literal_eval(value)[1][1]
        col_list = table.get_content_by_col_value(
            config.DOC_DIR,
            self.excel_name,
            self.sheet_name,
            col,
            col_value,
            self.col_index)
        for i in col_list:
            if i > max_value or i < min_value:
                agent.pri_excel(
                    self.excel_name,
                    self.sheet_name,
                    row=self.col_index_name)
                print("范围规则错误", i, ast.literal_eval(value)[1])

    # {"_In":{"Sequence":{"star":"[0,(1,11)]"}}}
    # star = 0取出当前表格一列，序列1到11中每个数都存在前面取出的一列中
    def sequence(self, _value):
        (key, value), = _value.items()
        col = key
        col_value = ast.literal_eval(value)[0]
        min_value = ast.literal_eval(value)[1][0]
        max_value = ast.literal_eval(value)[1][1]
        col_list = table.get_content_by_col_value(
            config.DOC_DIR,
            self.excel_name,
            self.sheet_name,
            col,
            col_value,
            self.col_index)
        for i in range(min_value, max_value + 1):
            if i not in col_list:
                agent.pri_excel(
                    self.excel_name,
                    self.sheet_name,
                    col=self.col_index_name)
                print("序列规则错误", i, value)

    # 当star=2的时候，本列（检查的这列）要属于[1,7,30]
    # {"_In":{"Whenassign":{"star":"[2,[1,30]]"}}}
    def whenassign(self, _value):
        (key, value), = _value.items()
        col = key
        col_value = ast.literal_eval(value)[0]
        lis_value = ast.literal_eval(value)[1]
        head = self.r_sheet.row_values(config.HEAD)
        col_index = head.index(col)
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            if agent.change_format(
                self.r_sheet.cell_value(
                    i, col_index)) == col_value:
                if agent.change_format(
                    self.r_sheet.cell_value(
                        i, self.col_index)) not in lis_value:
                    agent.pri_excel(
                        self.excel_name,
                        self.sheet_name,
                        row=i,
                        col=self.col_index_name)
                    print(
                        "该值{}错误，没有存在于{}".format(
                            agent.change_format(
                                self.r_sheet.cell_value(
                                    i,
                                    self.col_index)),
                            lis_value))

    # 当本表中指定A列值为多少时，B列的值要存在与另外 一个表的某一列
    # {"_In":{"Whenpoint":{"type_id":"[2,['/sys_card.xls','Sheet1','id',]]"}}}
    def whenpoint(self, _value):
        (key, value), = _value.items()
        col = key
        col_value = ast.literal_eval(value)[0]
        lis_value = ast.literal_eval(value)[1]
        d_excel = lis_value[0]
        d_sheet_name = lis_value[1]
        d_col = lis_value[2]
        r_head = self.r_sheet.row_values(config.HEAD)
        rcol_index = r_head.index(col)
        d_wbk = table.open_workbook(config.DOC_DIR, d_excel)
        d_sheet = d_wbk.sheet_by_name(d_sheet_name)
        d_head = d_sheet.row_values(config.HEAD)
        dcol_index = d_head.index(d_col)
        point_list = table.get_content_by_col(
            config.DOC_DIR, d_excel, d_sheet_name, dcol_index)
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            if not agent.pass_empty(i, self.r_sheet, rcol_index):
                continue
            if agent.change_format(
                self.r_sheet.cell_value(
                    i, rcol_index)) == col_value:
                if agent.change_format(
                    self.r_sheet.cell_value(
                        i, self.col_index)) not in point_list:
                    agent.pri_excel(
                        self.excel_name, self.sheet_name, i, self.col_index_name)
                    # 调用函数时,参数超长时,多行显示,首行不显示参数,余者按层次缩进显示
                    print(
                        "规则whenpoint {}：当本表中指定A列值为多少时，B列的值要存在与另外 一个表的某一列 {}".format(
                            _value, agent.change_format(
                                self.r_sheet.cell_value(
                                    i, self.col_index))))

    # 单元格中的每个值都存在于指定表格指定列
    # {"_In":{"Every":["/sys_card_skill.xls","Sheet1","id"]}}
    def every_in(self, _value):
        d_wbk = table.open_workbook(config.DOC_DIR, _value[0])
        d_sheet = d_wbk.sheet_by_name(_value[1])
        d_head = d_sheet.row_values(config.HEAD)
        d_index = d_head.index(_value[2])
        d_col_list = table.get_content_by_col(
            config.DOC_DIR, _value[0], _value[1], d_index)
        d_col_list1 = [str(j) for j in d_col_list]
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not self.r_sheet.cell_value(i, self.col_index):
                continue
            cell = re.split(
                r'[,]', str(
                    agent.change_format(
                        self.r_sheet.cell_value(
                            i, self.col_index))))
            for j in range(0, len(cell)):
                if str(cell[j]) not in d_col_list1:
                    agent.pri_excel(
                        self.excel_name, self.sheet_name, i, self.col_index_name)
                    print("规则：单元格中的每个值都存在于指定表格指定列。该错误单元格数据为{}--规则为{}". format(
                        str(self.r_sheet.cell_value(i, self.col_index)), _value))

    # {"_In": {"Allpoint": {"need_level": "[1,['/F副本表.xls','Sheet1','id']]"}}}
    # 检查本列单元格，必须存在于，指定表格指定字段=X的时候，指定另外一列中
    # 兼容101001,1201001的情况，会分别判断单个是否存在
    def allpoint(self, _value):
        (key, value), = _value.items()
        col = key
        col_value = ast.literal_eval(value)[0]
        lis_value = ast.literal_eval(value)[1]
        d_excel = lis_value[0]
        d_sheet_name = lis_value[1]
        d_col = lis_value[2]
        d_wbk = table.open_workbook(config.DOC_DIR, d_excel)
        # d_sheet = d_wbk.sheet_by_name(d_sheet_name)
        point_list = [str(k) for k in table.get_content_col_by_col2name(
            config.DOC_DIR, d_excel, d_sheet_name, d_col, col, col_value)]
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            temp = re.split(',', str(agent.change_format(
                self.r_sheet.cell_value(
                    i, self.col_index))))
            for j in temp:
                if j not in point_list:
                    agent.pri_excel(
                        self.excel_name,
                        self.sheet_name,
                        i,
                        self.col_index_name)
                    # 调用函数时,参数超长时,多行显示,首行不显示参数,余者按层次缩进显示
                    print("规则allpoint {}：本表指定列存在于另外一个表的某一列（当clo=col_value时的那一列值）{}".format(
                        _value,
                        agent.change_format(self.r_sheet.cell_value(i, self.col_index))))
                    break


class Equal(object):
    def __init__(self, *args, **kwargs):
        self.excel_name = kwargs["excel_name"]
        self.sheet_name = kwargs["sheet_name"]
        self.col_index = kwargs["col_index"]
        self.args = args
        self.r_wbk = table.open_workbook(config.DOC_DIR, self.excel_name)
        self.r_sheet = self.r_wbk.sheet_by_name(self.sheet_name)
        r_head = self.r_sheet.row_values(config.HEAD_CN)
        self.col_index_name = r_head[self.col_index]
        if isinstance(self.args[0], dict):
            (key, value), = self.args[0].items()
            if key == "All":
                self.all_equal(value)
            if key == "Part":
                self.part_equal(value)
            if key == "Count":
                self.count_equal(value)
            if key == "Dislocation":
                self.dislocation_equal(value)

    # {"_Equal":{"All":["/sys_artist.xls","Sheet1","real_name"]}}
    # 本列，全部一一等同于指定表格的那一列（位置一一对应）
    def all_equal(self, value):
        d_wbk = table.open_workbook(config.DOC_DIR, value[0])
        d_sheet = d_wbk.sheet_by_name(value[1])
        d_head = d_sheet.row_values(config.HEAD)
        d_index = d_head.index(value[2])
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not self.r_sheet.cell_value(i, self.col_index):
                continue
            if self.r_sheet.cell_value(
                    i,
                    self.col_index) != d_sheet.cell_value(
                    i,
                    d_index):
                agent.pri_excel(
                    self.excel_name,
                    self.sheet_name,
                    i,
                    self.col_index_name)
                print(
                    "规则:全部一一等同于指定表格的那一列, 数据为--{}--和--{}". format(
                        self.r_sheet.cell_value(
                            i, self.col_index), d_sheet.cell_value(
                            i, d_index), ))

    # 规则：当A列等于B列的值时，本列的值要等于C列
    # {"_Equal":{"Part":{"id":["/sys_artist.xls","Sheet1","name","cs_id"]}}}
    def part_equal(self, _value):
        (key, value), = _value.items()
        d_wbk = table.open_workbook(config.DOC_DIR, value[0])
        d_sheet = d_wbk.sheet_by_name(value[1])
        d_head = d_sheet.row_values(config.HEAD)
        d_index1 = d_head.index(value[2])
        same_index2 = d_head.index(value[3])
        r_wbk = table.open_workbook(config.DOC_DIR, self.excel_name)
        r_sheet = r_wbk.sheet_by_name(self.sheet_name)
        r_head = r_sheet.row_values(config.HEAD)
        same_id_index = r_head.index(key)
        for i in range(config.ROW_START, r_sheet.nrows):
            if not r_sheet.cell_value(i, self.col_index):
                continue
            if not r_sheet.cell_value(i, same_id_index):
                continue
            for j in range(config.ROW_START, d_sheet.nrows):
                if str(
                    r_sheet.cell_value(
                        i,
                        same_id_index)) == str(
                    d_sheet.cell_value(
                        j,
                        same_index2)):
                    if str(
                        r_sheet.cell_value(
                            i,
                            self.col_index)) != str(
                        d_sheet.cell_value(
                            j,
                            d_index1)):
                        agent.pri_excel(
                            self.excel_name, self.sheet_name, i, self.col_index)
                        print(
                            "规则：当A列等于B列的值时，本列的值要等于C列", str(
                                r_sheet.cell_value(
                                    i, self.col_index)))

    # {"_Equal":{"Count":"(0,10)"}}
    # 本检查列，值为0的数量有10个
    def count_equal(self, _value):
        result = 0
        point_value = ast.literal_eval(_value)[0]
        point_count = ast.literal_eval(_value)[1]
        col_list = table.get_content_by_col(
            config.DOC_DIR,
            self.excel_name,
            self.sheet_name,
            self.col_index)
        d_col_list1 = [str(j) for j in col_list]
        for i in d_col_list1:
            if i == str(point_value):
                result += 1
        if str(result) != str(point_count):
            agent.pri_excel(
                self.excel_name,
                self.sheet_name,
                row='',
                col=self.col_index_name)
            print(
                "规则错误：本列检查值为{}的数量为{},实际为{}".format(
                    point_value,
                    point_count,
                    result))

    # 错位相等：本列去除头，id一列去除尾，其他一一对应
    # {"_Equal":{"Dislocation":["/sys_artist.xls","Sheet1","id", -1]}}
    def dislocation_equal(self, value):
        d_wbk = table.open_workbook(config.DOC_DIR, value[0])
        d_sheet = d_wbk.sheet_by_name(value[1])
        d_head = d_sheet.row_values(config.HEAD)
        d_index = d_head.index(value[2])
        dislocation = value[3]
        # print(dislocation, type(dislocation))
        # config.ROW_START+1去除头
        for i in range(config.ROW_START+1, self.r_sheet.nrows):
            if not self.r_sheet.cell_value(i, self.col_index):
                continue
            if self.r_sheet.cell_value(
                    i,
                    self.col_index) != d_sheet.cell_value(
                i+dislocation,
                d_index):
                agent.pri_excel(
                    self.excel_name,
                    self.sheet_name,
                    i,
                    self.col_index_name)
                print(
                    "规则:错位相等, 数据为--{}--和--{}".format(
                        self.r_sheet.cell_value(
                            i, self.col_index), d_sheet.cell_value(
                            i, d_index), ))


class Common(object):
    @staticmethod
    def list_only(list):
        b = dict(Counter(list))
        no_only = [key for key, value in b.items() if value > 1]
        if no_only:
            return no_only
        else:
            return

    @staticmethod
    def change_format(value):
        pattern = re.compile(r'\d*')
        if value == "":
            return value
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        # print(value, type(value))
        if re.fullmatch(pattern, value):
            return int(value)
        return value

    @staticmethod
    def pri_excel(name, sheet, row='', col=''):
        if row == '' and col == '':
            print(
                "表格位置----------------------------------{}-------------------------{}".format(name, sheet,))
        else:
            print(
                "表格位置----------------------------------{}--------------------------{}--行{}--列{}".format(
                    name,
                    sheet,
                    row,
                    col))

    # 排除空单元格
    @staticmethod
    def pass_empty(i, sheet, col_index):
        if not sheet.cell_value(i, col_index):
            return
        if sheet.cell(i, col_index).ctype == 6:
            return
        if str(sheet.cell_value(i, col_index)) == '0':
            return
        return True

    # 表达式规则专用
    @staticmethod
    def analytic_expression(value, expression):
        temp = str(value) + " "
        if 'x' in expression:
            # print(re.sub('x', temp, expression), eval(re.sub('x', temp, expression)))
            return eval(re.sub('x', temp, expression))


class Match(object):
    def __init__(self, *args, **kwargs):
        self.excel_name = kwargs["excel_name"]
        self.sheet_name = kwargs["sheet_name"]
        self.col_index = kwargs["col_index"]
        self.args = args
        # r_wbk  指数据配置表中对应规则表的那个表（也就是数据表）
        # d_wbk  指数据配置表中对应规则表配置的规则所指向的那个表（也就是我配的规则里指向的那个表）
        self.r_wbk = table.open_workbook(config.DOC_DIR, self.excel_name)
        self.r_sheet = self.r_wbk.sheet_by_name(self.sheet_name)
        r_head = self.r_sheet.row_values(config.HEAD_CN)
        self.col_index_name = r_head[self.col_index]
        if isinstance(self.args[0], dict):
            (key, value), = self.args[0].items()
            # pattern = re.compile(key)
            self.match_if(key, value)
        else:
            # pattern = re.compile(self.args[0])
            self.match(self.args[0])

    # {"_Match":"^\d$"}
    # 1:43;2:71;3:68;4:40;5:98  匹配规则：(\d:\d+;)*\d:\d+
    def match(self, pattern):
        pat = re.compile(pattern)
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not self.r_sheet.cell_value(i, self.col_index):
                continue
            if self.r_sheet.cell(i, self.col_index) == 6:
                continue
            if not re.match(
                pat, str(
                    agent.change_format(
                        self.r_sheet.cell_value(
                    i, self.col_index)))):
                agent.pri_excel(
                    self.excel_name,
                    self.sheet_name,
                    i,
                    self.col_index_name)
                print("正则匹配失败：{}".format(str(agent.change_format(
                    self.r_sheet.cell_value(i, self.col_index)))))

    # {"_Match":{"^\\d*:\\d*;?$":["type",1]}}
    # 当type一列满足值为1的时候，所检查的本列要满足正则表达式
    def match_if(self, pattern, condition):
        pat = re.compile(pattern)
        col = condition[0]
        col_value = condition[1]
        head = self.r_sheet.row_values(config.HEAD)
        col_index = head.index(col)
        for i in range(config.ROW_START, self.r_sheet.nrows):
            # if not agent.pass_empty(i, self.r_sheet, self.col_index):
            #     continue
            if not agent.pass_empty(i, self.r_sheet, col_index):
                continue
            if agent.change_format(
                self.r_sheet.cell_value(
                    i, col_index)) == col_value:
                if not re.match(
                    pat, str(
                        agent.change_format(
                            self.r_sheet.cell_value(
                                i, self.col_index)))):
                    agent.pri_excel(
                        self.excel_name, self.sheet_name, i, self.col_index_name)
                    print("正则匹配失败：{}".format(str(agent.change_format(
                        self.r_sheet.cell_value(i, self.col_index)))))


class Dictionary(object):
    def __init__(self, *args, **kwargs):
        self.excel_name = kwargs["excel_name"]
        self.sheet_name = kwargs["sheet_name"]
        self.col_index = kwargs["col_index"]
        self.args = args
        self.r_wbk = table.open_workbook(config.DOC_DIR, self.excel_name)
        self.r_sheet = self.r_wbk.sheet_by_name(self.sheet_name)
        r_head = self.r_sheet.row_values(config.HEAD_CN)
        self.col_index_name = r_head[self.col_index]
        if isinstance(self.args[0], dict):
            (key, value), = self.args[0].items()
            if key == "Keyin":
                self.keyin(value)
            if key == "Keyinlist":
                self.keyinlist(value)
            if key == "Whenkeyin":
                self.whenkeyin(value)
            if key == "Comma":
                self.comma(value)

    # 字典的key in 指定表格位置的一列
    # {"_Dict":{"Keyin":["/sys_goods.xls","Sheet1","id"]}}
    def keyin(self, _value):
        d_wbk = table.open_workbook(config.DOC_DIR, _value[0])
        d_sheet = d_wbk.sheet_by_name(_value[1])
        d_head = d_sheet.row_values(config.HEAD)
        d_index = d_head.index(_value[2])
        d_col_list = table.get_content_by_col(
            config.DOC_DIR, _value[0], _value[1], d_index)
        d_col_list = [str(i) for i in d_col_list]
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            cell = re.split(
                r'[,;:]', str(
                    self.r_sheet.cell_value(
                        i, self.col_index)))
            for j in range(0, len(cell), 2):
                if cell[j] not in d_col_list:
                    agent.pri_excel(
                        self.excel_name, self.sheet_name, i, self.col_index_name)
                    print(
                        self.r_sheet.cell_value(
                            i, self.col_index), "keyin规则")

    # 形如20101,20102,20103
    # {"_Dict":{"Comma":["/sys_goods.xls","Sheet1","id"]}}
    def comma(self, _value):
        d_wbk = table.open_workbook(config.DOC_DIR, _value[0])
        d_sheet = d_wbk.sheet_by_name(_value[1])
        d_head = d_sheet.row_values(config.HEAD)
        d_index = d_head.index(_value[2])
        d_col_list = table.get_content_by_col(
            config.DOC_DIR, _value[0], _value[1], d_index)
        d_col_list = [str(i) for i in d_col_list]
        for i in range(config.ROW_START, self.r_sheet.nrows):
            cell_value = self.r_sheet.cell_value(i, self.col_index)
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            if ',' not in str(cell_value):
                cell = [str(agent.change_format(cell_value))]
            else:
                cell = re.split(r'[,]', str(cell_value))
            for j in range(0, len(cell)):
                if cell[j] not in d_col_list:
                    agent.pri_excel(
                        self.excel_name, self.sheet_name, i, self.col_index_name)
                    print(self.r_sheet.cell_value(i, self.col_index), "规则：形如20101,20102,20103，每个值要存在于指定列", _value)

    # 字典的key in你指定的一列
    # {"_Dict":{"Keyinlist":[1,2,3,4,5]}}
    def keyinlist(self, _value):
        _value = [str(i) for i in _value]
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not self.r_sheet.cell_value(i, self.col_index):
                continue
            if self.r_sheet.cell(i, self.col_index) == 6:
                continue
            cell = re.split(
                r'[;:]', str(
                    self.r_sheet.cell_value(
                        i, self.col_index)))
            for j in range(0, len(cell) - 1, 2):
                if cell[j] not in _value:
                    agent.pri_excel(
                        self.excel_name, self.sheet_name, i, self.col_index_name)
                    print(
                        "规则错误keyinlist--{}".format(
                            agent.change_format(
                                self.r_sheet.cell_value(
                                    i, self.col_index))))

    # {"_Dict":{"Whenkeyin":{"event":["Gift",["/sys_goods.xls","Sheet1","id"]]}}}
    # 当列event值为Gift时，本列的字典key存在于指定一列
    def whenkeyin(self, _value):
        # {"event":["Gift",["/sys_goods.xls","Sheet1","id"]]}
        (key, _value), = _value.items()
        r_head = self.r_sheet.row_values(config.HEAD)
        r_index = r_head.index(key)
        d_excel = _value[1][0]
        d_sheet_name = _value[1][1]
        d_col = _value[1][2]
        d_col_list = table.get_content_by_col_name(
            config.DOC_DIR, d_excel, d_sheet_name, d_col)
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            if not agent.pass_empty(i, self.r_sheet, r_index):
                continue
            if agent.change_format(
                self.r_sheet.cell_value(
                    i, r_index)) == _value[0]:
                if not agent.pass_empty(i, self.r_sheet, self.col_index):
                    continue
                cell = re.split(
                    r'[;:]', str(
                        self.r_sheet.cell_value(
                            i, self.col_index)))
                for j in range(0, len(cell), 2):
                    if cell[j] not in [str(k) for k in d_col_list]:
                        agent.pri_excel(
                            self.excel_name, self.sheet_name, i, self.col_index_name)
                        print(
                            "规则错误Whenkeyin--{}".format(
                                agent.change_format(
                                    self.r_sheet.cell_value(
                                        i, self.col_index))))


class Exception():
    pass


class Condition(object):
    def __init__(self, *args, **kwargs):
        self.excel_name = kwargs["excel_name"]
        self.sheet_name = kwargs["sheet_name"]
        self.col_index = kwargs["col_index"]
        self.args = args
        self.r_wbk = table.open_workbook(config.DOC_DIR, self.excel_name)
        self.r_sheet = self.r_wbk.sheet_by_name(self.sheet_name)
        r_head = self.r_sheet.row_values(config.HEAD_CN)
        self.col_index_name = r_head[self.col_index]
        if isinstance(self.args[0], dict):
            (key, value), = self.args[0].items()
            if key == "All":
                self.all_condition(value)
            if key == "Appoint":
                self.appoint_condition(value)
            if key == "Oneof":
                self.oneof_condition(value)

    # 条件，万能大法，当group_type=1时，取出本列的值，满足：其中一个数值!=0即可
    # {"_Condition":{"Oneof":["('group_type', 1)","x!=0"]}}
    def oneof_condition(self, _value):
        col1 = ast.literal_eval(_value[0])[0]
        col1_value = ast.literal_eval(_value[0])[1]

        col_list = table.get_content_by_col_value(
            config.DOC_DIR,
            self.excel_name,
            self.sheet_name,
            col1,
            col1_value,
            self.col_index)
        for x in col_list:
            if agent.analytic_expression(x, _value[1]):
                return
                # 如果有一个满足条件，检查成功，结束检查
        agent.pri_excel(
            self.excel_name,
            self.sheet_name,
            row='',
            col=self.col_index_name)
        print("规则错误：当a列=b时，所检查的本列要满足其中一个至少符合条件", _value)

    # 条件，万能大法，本列的值，每个都满足：!=0
    # {"_Condition":{"All":"x!=0"}}
    def all_condition(self, _value):
        expression = _value
        for i in range(config.ROW_START, self.r_sheet.nrows):
            if not agent.pass_empty(i, self.r_sheet, self.col_index):
                continue
            if agent.analytic_expression(
                self.r_sheet.cell_value(
                    i, self.col_index), expression):
                continue
            agent.pri_excel(
                self.excel_name,
                self.sheet_name,
                i,
                self.col_index_name)
            print("规则错误：本列的值，每个都满足条件", _value)


class Increasing(object):
    def __init__(self, *args, **kwargs):
        self.excel_name = kwargs["excel_name"]
        self.sheet_name = kwargs["sheet_name"]
        self.col_index = kwargs["col_index"]
        self.args = args
        self.r_wbk = table.open_workbook(config.DOC_DIR, self.excel_name)
        self.r_sheet = self.r_wbk.sheet_by_name(self.sheet_name)
        r_head = self.r_sheet.row_values(config.HEAD_CN)
        self.col_index_name = r_head[self.col_index]
        temp = {"col_increase": "col_increase",
                }
        if isinstance(self.args[0], dict):
            (key, value), = self.args[0].items()
            self.__getattribute__(temp[key])(value)
        elif self.args[0] == "col_increase":
            self.col_increase()

    def col_increase(self):
        d_col = table.get_content_by_col(
            config.DOC_DIR,
            self.excel_name,
            self.sheet_name,
            self.col_index)
        if not all([x < y for x, y in zip(d_col, d_col[1:])]):
            agent.pri_excel(
                name=self.excel_name,
                sheet=self.sheet_name,
                col=self.col_index_name)
            print("规则错误：第{}列要满足递增".format(str(self.col_index)))


table = Table()
agent = Common()
