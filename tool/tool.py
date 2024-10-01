import config
import xlrd
import re
import math
from table_operation import Table

tb = Table()
card = '/K卡牌表.xls'
card_level = '/K卡牌星级表.xls'

class Tool(object):
    def __init__(self):
        tb = Table()
    @staticmethod
    def change_str(value):
        result = {}
        if value:
            temp = re.split(':|;', str(value))
            for i in range(0, len(temp), 2):
                result[temp[i]] = temp[i+1]
            return result
        else:
            return


    def card_attr(self):
        yuansu = {
            "1": "唱功",
            "2": "舞艺",
            "3": "演技",
            "4": "口才",
            "5": "交际",
        }
        # 卡牌等级属性=[（等级*（成长属性+突破属性）+初始值]/100
        card = '/K卡牌表.xls'
        card_break = '/K卡牌突破表.xls'
        card_id = 201303
        tupo = tb.get_cell_value(config.DOC_DIR, "/K卡牌突破表.xls", "Sheet1", "card_id", card_id, "times", False)
        level = tb.get_cell_value(config.DOC_DIR, "/K卡牌突破表.xls", "Sheet1", "card_id", card_id, "max_level", False)
        base_attr = tb.get_cell_value(config.DOC_DIR, "/K卡牌表.xls", "Sheet1", "id", card_id, "base_attr",)
        base = Tool.change_str(base_attr)
        chengzhang = Tool.change_str(tb.get_cell_value(config.DOC_DIR, "/K卡牌表.xls", "Sheet1", "id", card_id, "attr",))
        length = len(tupo)


        for i in range(length):
            print("现在是突破{}:".format(tupo[i]))
            if tupo[i] == 0:
                min_level = 1
            else:
                min_level= level[i-1]
            tupo_attr = Tool.change_str(tb.get_cell_value2(config.DOC_DIR, "/K卡牌突破表.xls", "Sheet1", "times", tupo[i], "card_id", card_id, "attr"))
            if not tupo_attr:
                tupo_attr = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
            # print(min_level,level[i],tupo[i],type(tupo[i]))
            for j in range(min_level, level[i]+1):
                print("等级是{}".format(j))
                for key,value in base.items():
                    temp = j*(int(tupo_attr[key])+int(chengzhang[key]))+int(base[key])
                    print(yuansu[key], temp/100)


test = Tool()
test.card_attr()

